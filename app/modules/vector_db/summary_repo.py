from weaviate.classes.config import Property, DataType
from weaviate.classes.tenants import Tenant
from weaviate.classes.query import MetadataQuery
from app.schema.vector_db import RagSearchModeEnum
from app.vector_db.weaviate_client import get_weaviate_client
from app.ai_models.embeddings import aembed_query

COLLECTION_NAME = "Summary"


class SummaryTenantMgt:
    """
    租户管理类，用于管理租户的创建、删除、获取等操作
    """

    def __init__(self):
        self.client = get_weaviate_client()
        self.collection = self.client.collections.get(COLLECTION_NAME)

    async def create_tenant(self, tenant_name: str):
        """
        创建租户
        """
        await self.collection.tenants.create(tenants=[Tenant(name=tenant_name)])

    async def get_tenants(self):
        """
        获取所有租户
        """
        return await self.collection.tenants.get()

    async def remove_tenant(self, tenant_name: str):
        """
        删除租户
        """
        await self.collection.tenants.remove(tenant_name)


class SummaryRepo:
    """
    摘要管理类，基于租户管理摘要的添加、获取、更新、删除等操作
    """

    def __init__(self, tenant_name: str):
        self.client = get_weaviate_client()
        self.collection = self.client.collections.get(COLLECTION_NAME)
        self.tenant_coll = self.collection.with_tenant(tenant_name)

    async def add_summary(self, summary: str):
        """
        添加摘要，返回插入的id
        """
        summary_embed = await aembed_query(summary)
        return self.tenant_coll.data.insert(
            properties={
                "summary": summary,
            },
            vector={
                "vector": summary_embed,
            },
        )

    async def get_summary(self, id: str):
        """根据id获取摘要对象"""
        return await self.tenant_coll.query.fetch_object_by_id(id)

    async def update_summary(self, summary: str):
        # TODO: 更新摘要
        pass

    async def delete_summary(self, id: str):
        return await self.tenant_coll.data.delete_by_id(id)

    async def rag_search(
        self,
        query: str,
        mode: RagSearchModeEnum = RagSearchModeEnum.similarity,
        distance: float = 0.5,
        k: int = 5,
    ):
        """
        rag搜索，返回相似度最高的k个摘要，支持相似度搜索和混合搜索
        """
        if mode == RagSearchModeEnum.similarity:
            return await self.similarity_search(query, distance, k)
        elif mode == RagSearchModeEnum.hybrid:
            return await self.hybrid_search(query, distance, k)

    async def similarity_search(self, query: str, distance: float = 0.5, k: int = 5):
        """
        相似度搜索，返回相似度最高的k个摘要
        """
        query_embed = await aembed_query(query)
        return await self.tenant_coll.query.near_vector(
            near_vector=query_embed,
            limit=k,
            distance=distance,
            target_vector="vector",
            return_metadata=MetadataQuery(
                distance=True, creation_time=True, last_update_time=True
            ),
        )

    async def hybrid_search(self, query: str, distance: float = 0.5, k: int = 5):
        """
        混合搜索，返回相似度最高的k个摘要
        """
        query_embed = await aembed_query(query)
        return await self.tenant_coll.query.hybrid(
            query=query,
            vector=query_embed,
            target_vector="vector",
            max_vector_distance=distance,
            limit=k,
            return_metadata=MetadataQuery(
                distance=True, creation_time=True, last_update_time=True
            ),
        )
