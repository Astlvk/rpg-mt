from warnings import deprecated
from uuid import UUID
from weaviate.classes.config import DataType, Property
from weaviate.classes.tenants import Tenant
from weaviate.classes.query import MetadataQuery, Sort, Filter, QueryNested
from weaviate.collections.classes.grpc import PROPERTIES
from app.schema.summary import (
    SummarySearchModeEnum,
    SummarySearchResult,
    TenantInfo,
    SummaryDataModel,
    MergedSummary,
    SummaryDataModelUpdate,
)
from app.schema.api import ApiResponse
from app.schema.summary import SummaryTypeEnum
from app.vector_db.weaviate_client import get_weaviate_client
from app.ai_models.embeddings import aembed_query

COLLECTION_NAME = "Summary"


class SummaryCollection:
    def __init__(self):
        self.client = get_weaviate_client()
        self.collection = self.client.collections.get(COLLECTION_NAME)

    async def update_collection(self):
        """
        更新集合定义，根据需要自行编码调用。
        """
        await self.collection.config.update(
            property_descriptions={
                "marged_summary": "废弃的！！！由于拼写错误，废弃的属性。",
            }
        )

    async def add_new_property(self):
        """
        添加新的属性，后续有新增属性时，咨询修改该方法并调用
        """
        await self.collection.config.add_property(
            Property(
                name="type",
                data_type=DataType.TEXT,
                description="摘要类型，可以用来划分如：摘要、对话、剧情、角色等",
            ),
        )


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

    async def remove_tenant(self, tenant_name: str):
        """
        删除租户
        """
        await self.collection.tenants.remove(tenant_name)

    async def get_tenants(self):
        """
        获取所有租户，并为每个租户添加数据量字段
        """
        tenants = await self.collection.tenants.get()
        tenants_dict: dict[str, TenantInfo] = {}

        for key, tenant in tenants.items():
            tenant_coll = self.collection.with_tenant(key)
            data_count = await tenant_coll.length()
            print(tenant)
            tenants_dict[key] = {
                "name": key,
                "data_count": data_count,
                "activityStatus": tenant.activityStatus,
            }

        return tenants_dict


class SummaryTenantRepo:
    """
    摘要管理类，基于租户管理摘要的添加、获取、更新、删除等操作
    """

    def __init__(self, tenant_name: str):
        self.client = get_weaviate_client()
        self.collection = self.client.collections.use(
            COLLECTION_NAME, data_model_properties=SummaryDataModel
        )
        self.collection_update = self.client.collections.use(
            COLLECTION_NAME, data_model_properties=SummaryDataModelUpdate
        )
        self.tenant_coll = self.collection.with_tenant(tenant_name)
        self.tenant_coll_update = self.collection_update.with_tenant(tenant_name)
        self.return_properties: PROPERTIES = [
            "summary",
            "type",
            "turn",
            QueryNested(name="merged_summary", properties=["summary", "turn"]),
        ]

    async def add_summary(
        self,
        summary: str,
        turn: int | None = None,
        summary_type: SummaryTypeEnum | None = None,
        merged_summary: list[MergedSummary] | None = None,
    ):
        """
        添加摘要，向量化，返回插入的id
        """
        summary_embed = await aembed_query(summary)
        return await self.tenant_coll.data.insert(
            properties={
                "summary": summary,
                "turn": turn,
                "type": summary_type,
                "merged_summary": merged_summary,
            },
            vector={
                "vector": summary_embed,
            },
        )

    async def update_summary(
        self,
        uuid: str,
        summary: str,
        turn: int | None = None,
        summary_type: SummaryTypeEnum | None = None,
    ):
        # 更新摘要
        summary_embed = await aembed_query(summary)
        return await self.tenant_coll_update.data.update(
            uuid=uuid,
            properties={
                "summary": summary,
                "turn": turn,
                "type": summary_type,
            },
            vector={
                "vector": summary_embed,
            },
        )

    async def delete_summary(self, id: str):
        return await self.tenant_coll.data.delete_by_id(id)

    async def delete_summary_by_uuids(self, uuids: list[str] | list[UUID]):
        """
        根据uuids删除摘要
        """
        return await self.tenant_coll.data.delete_many(
            where=Filter.by_id().contains_any(uuids)
        )

    async def get_summary_by_id(self, id: str):
        """
        根据id获取摘要对象
        """
        return await self.tenant_coll.query.fetch_object_by_id(id)

    async def get_summaries(self, limit: int = 10):
        """
        获取所有摘要，limit为返回数量
        """
        return await self.tenant_coll.query.fetch_objects(
            sort=Sort.by_update_time(ascending=False),
            limit=limit,
            return_metadata=MetadataQuery.full(),
            return_properties=self.return_properties,
        )

    async def get_summaries_offset(self, size: int = 10, page: int = 1):
        """
        获取所有摘要，offset分页形式，size为每页数量，page为页码
        """
        assert page >= 1 and size >= 1
        total = await self.tenant_coll.length()
        res = await self.tenant_coll.query.fetch_objects(
            sort=Sort.by_update_time(ascending=False),
            limit=size,
            offset=(page - 1) * size,
            return_metadata=MetadataQuery.full(),
            return_properties=self.return_properties,
        )

        res_data = []
        for obj in res.objects:
            res_data.append(
                {
                    "uuid": str(obj.uuid),
                    "summary": str(obj.properties["summary"]),
                    "turn": obj.properties.get("turn", None),
                    "merged_summary": obj.properties.get("merged_summary", None),
                    "created_at": (
                        obj.metadata.creation_time.astimezone().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if obj.metadata.creation_time
                        else None
                    ),
                    "updated_at": (
                        obj.metadata.last_update_time.astimezone().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if obj.metadata.last_update_time
                        else None
                    ),
                }
            )

        return {"total": total, "data": res_data}

    async def get_summaries_by_cursor(
        self, cursor: str | None = None, limit: int = 100
    ):
        """
        基于游标的分页查询，cursor为游标，limit为返回数量
        """
        total = await self.tenant_coll.length()
        res = await self.tenant_coll.query.fetch_objects(
            limit=limit,
            after=cursor,
            return_metadata=MetadataQuery.full(),
            return_properties=self.return_properties,
        )

        res_data = []
        for obj in res.objects:
            res_data.append(
                {
                    "uuid": str(obj.uuid),
                    "summary": str(obj.properties["summary"]),
                    "turn": obj.properties.get("turn", None),
                    "merged_summary": obj.properties.get("merged_summary", None),
                    "created_at": (
                        obj.metadata.creation_time.astimezone().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if obj.metadata.creation_time
                        else None
                    ),
                    "updated_at": (
                        obj.metadata.last_update_time.astimezone().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if obj.metadata.last_update_time
                        else None
                    ),
                }
            )

        return {"total": total, "data": res_data}

    async def summary_search(
        self,
        query: str,
        mode: SummarySearchModeEnum = SummarySearchModeEnum.similarity,
        distance: float = 0.5,
        top_k: int = 10,
    ):
        """
        向量搜索，返回相似度最高的k个摘要，支持相似度搜索和混合搜索
        """
        res = None
        if mode == SummarySearchModeEnum.keyword:
            res = await self.keyword_search(query, top_k)
        elif mode == SummarySearchModeEnum.similarity:
            res = await self.similarity_search(query, distance, top_k)
        elif mode == SummarySearchModeEnum.hybrid:
            res = await self.hybrid_search(query, distance, top_k)

        res_data: list[SummarySearchResult] = []
        for obj in res.objects if res else []:
            res_data.append(
                {
                    "uuid": str(obj.uuid),
                    "summary": obj.properties["summary"],
                    "turn": obj.properties.get("turn", None),
                    "type": obj.properties.get("type", None),
                    "merged_summary": obj.properties.get("merged_summary", None),
                    "created_at": (
                        obj.metadata.creation_time.astimezone().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if obj.metadata.creation_time
                        else None
                    ),
                    "updated_at": (
                        obj.metadata.last_update_time.astimezone().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if obj.metadata.last_update_time
                        else None
                    ),
                    "score": obj.metadata.score,
                    "distance": obj.metadata.distance,
                }
            )

        return ApiResponse(total=len(res_data), data=res_data)

    async def keyword_search(self, query: str, top_k: int = 10):
        """
        关键字搜索，返回包含关键字的摘要
        """
        return await self.tenant_coll.query.bm25(
            query=query,
            query_properties=["summary"],
            limit=top_k,
            return_metadata=MetadataQuery.full(),
            return_properties=self.return_properties,
        )

    async def similarity_search(
        self, query: str, distance: float = 0.5, top_k: int = 10
    ):
        """
        相似度搜索，返回相似度最高的k个摘要
        """
        query_embed = await aembed_query(query)
        return await self.tenant_coll.query.near_vector(
            near_vector=query_embed,
            limit=top_k,
            distance=distance,
            target_vector="vector",
            return_metadata=MetadataQuery.full(),
            return_properties=self.return_properties,
        )

    async def hybrid_search(self, query: str, distance: float = 0.5, top_k: int = 10):
        """
        混合搜索，返回相似度最高的k个摘要
        """
        query_embed = await aembed_query(query)
        return await self.tenant_coll.query.hybrid(
            query=query,
            query_properties=["summary"],
            vector=query_embed,
            target_vector="vector",
            max_vector_distance=distance,
            limit=top_k,
            return_metadata=MetadataQuery.full(),
            return_properties=self.return_properties,
        )
