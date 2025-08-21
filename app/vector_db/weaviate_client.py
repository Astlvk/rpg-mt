"""
Weaviate 客户端
提供 Weaviate 数据库的初始化、获取和关闭功能
"""

import os
import weaviate
import logging
from weaviate.client import WeaviateClient, WeaviateAsyncClient
from weaviate.connect import ConnectionParams
from weaviate.classes.init import Auth, AdditionalConfig, Timeout

client: WeaviateAsyncClient | None = None


async def init_weaviate_client() -> WeaviateAsyncClient:
    """
    初始化 Weaviate 客户端，应用启动时调用一次
    """
    try:
        global client
        if client is None:
            client = weaviate.WeaviateAsyncClient(
                connection_params=ConnectionParams.from_params(
                    http_host=os.getenv("WEAVIATE_HOST", "127.0.0.1"),
                    http_port=int(os.getenv("WEAVIATE_PORT", 4900)),
                    http_secure=False,
                    grpc_host=os.getenv("WEAVIATE_HOST", "127.0.0.1"),
                    grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", 50051)),
                    grpc_secure=False,
                ),
                auth_client_secret=Auth.api_key(
                    os.getenv("WEAVIATE_API_KEY", "rpg-mt-hello-world")
                ),
                additional_config=AdditionalConfig(
                    timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
                ),
                skip_init_checks=False,
            )
        await client.connect()
        return client
    except Exception as e:
        logging.exception(e)
        raise e


def get_weaviate_client() -> WeaviateAsyncClient:
    """
    获取全局 Weaviate 客户端实例
    """
    if client is None:
        raise RuntimeError(
            "Weaviate client not initialized. Call init_weaviate_client() first."
        )
    return client


async def close_weaviate_client():
    """
    关闭 Weaviate 客户端
    """
    try:
        client = get_weaviate_client()
        await client.close()
    except Exception as e:
        logging.exception(e)
        raise e
