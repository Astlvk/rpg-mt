from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.modules.static_service import run as run_static_service
from app.utils.logger import LoggerConfig
from app.vector_db import weaviate_client
from app.modules.vector_db.collection_service import create_collections
from app.modules.common import router as router_common
from app.modules.chat import router as router_chat
from app.modules.vector_db import router as router_vector_db, router_summary
from app.modules.embedding import router as router_embedding
# from app.modules.vector_db.summary_repo import SummaryCollection


@asynccontextmanager
async def lifespan(app: FastAPI):
    LoggerConfig()
    # 这里初始化数据库
    await weaviate_client.init_weaviate_client()
    await create_collections()
    # await SummaryCollection().add_new_property()
    print("app init")
    yield
    # 这可以做清理工作
    await weaviate_client.close_weaviate_client()
    print("app clean")


app = FastAPI(lifespan=lifespan)

# 创建根路由器（带全局前缀）
root_router = APIRouter(prefix="/rpg-mt")

# 配置 CORS 中间件，配合scoketio的话，fastapi不能配置相同的跨域条件
# 不然web端会报错：
# The 'Access-Control-Allow-Origin' header contains multiple values 'http://localhost:8082, *',
# but only one is allowed.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名进行跨域请求
    allow_credentials=False,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

root_router.include_router(router_common.router, prefix="/common", tags=["Common"])
root_router.include_router(router_chat.router, prefix="/chat", tags=["Chat"])
root_router.include_router(
    router_embedding.router, prefix="/embedding", tags=["Embedding"]
)
root_router.include_router(
    router_vector_db.router, prefix="/vector_db", tags=["VectorDB"]
)
root_router.include_router(
    router_summary.router, prefix="/vector_db", tags=["VectorDB Summary"]
)

# 挂载根路由器到主应用
app.include_router(root_router)

# 挂载静态文件
run_static_service(app)

if __name__ == "__main__":
    print("world")
