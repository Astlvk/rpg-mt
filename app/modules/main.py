from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger import LoggerConfig
from app.vector_db import weaviate_client
from app.modules.common import router as common_router
from app.modules.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    LoggerConfig()
    # 这里初始化数据库
    weaviate_client.init_weaviate_client()
    print("app init")
    yield
    # 这可以做清理工作
    weaviate_client.close_weaviate_client()
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

root_router.include_router(common_router.router, prefix="/common", tags=["Common"])
root_router.include_router(chat_router.router, prefix="/chat", tags=["Chat"])

# 挂载根路由器到主应用
app.include_router(root_router)

if __name__ == "__main__":
    print("world")
