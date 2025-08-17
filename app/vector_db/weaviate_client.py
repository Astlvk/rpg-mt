"""
Weaviate 客户端
提供 Weaviate 数据库的初始化、获取和关闭功能
"""

import os
import weaviate
import logging
from weaviate.client import WeaviateClient
from weaviate.classes.init import Auth, AdditionalConfig, Timeout

client: WeaviateClient | None = None


def init_weaviate_client() -> WeaviateClient:
    """
    初始化 Weaviate 客户端，应用启动时调用一次
    """
    try:
        global client
        if client is None:
            client = weaviate.connect_to_local(
                host=os.getenv("WEAVIATE_HOST", "127.0.0.1"),
                port=int(os.getenv("WEAVIATE_PORT", 4900)),
                auth_credentials=Auth.api_key(
                    os.getenv("WEAVIATE_API_KEY", "rpg-mt-hello-world")
                ),  # 鉴权
                additional_config=AdditionalConfig(
                    timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
                ),
            )
        return client
    except Exception as e:
        logging.exception(e)
        raise e


def get_weaviate_client() -> WeaviateClient:
    """
    获取全局 Weaviate 客户端实例
    """
    if client is None:
        raise RuntimeError(
            "Weaviate client not initialized. Call init_weaviate_client() first."
        )
    return client


def close_weaviate_client():
    """
    关闭 Weaviate 客户端
    """
    try:
        client = get_weaviate_client()
        client.close()
    except Exception as e:
        logging.exception(e)
        raise e
