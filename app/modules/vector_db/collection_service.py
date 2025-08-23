from weaviate.classes.config import Property, DataType, Configure, Tokenization
from weaviate.collections.classes.config_vectors import _VectorConfigCreate
from app.vector_db.weaviate_client import get_weaviate_client
from .summary_repo import COLLECTION_NAME


class CollectionService:
    def __init__(self):
        self.client = get_weaviate_client()

    async def create_collection(
        self,
        name: str,
        description: str,
        properties: list[Property],
        vector_config: list[_VectorConfigCreate] = [
            Configure.Vectors.self_provided(name="vector"),
        ],
        multi_tenancy: bool = False,
    ):
        if not await self.client.collections.exists(name):
            await self.client.collections.create(
                name=name,
                description=description,
                properties=properties,
                multi_tenancy_config=Configure.multi_tenancy(enabled=multi_tenancy),
                vector_config=vector_config,
            )
            print(f"Collection {name} created")
        else:
            print(f"Collection {name} already exists")

    async def get_all_collection(self):
        return await self.client.collections.list_all()

    async def delete_collection(self, name: str):
        return await self.client.collections.delete(name)


async def create_collections():
    coll_service = CollectionService()
    await coll_service.create_collection(
        name=COLLECTION_NAME,
        description="摘要",
        properties=[
            Property(
                name="summary",
                data_type=DataType.TEXT,
                tokenization=Tokenization.GSE,
            ),
        ],
        vector_config=[
            Configure.Vectors.self_provided(name="vector"),
        ],
        multi_tenancy=True,
    )
