from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def run(app: FastAPI):
    DIST_DIR = Path("web_ui")
    # 静态文件
    app.mount("/web_ui", StaticFiles(directory="web_ui", html=True), name="web_ui")

    # 入口
    @app.get("/")
    async def app_index():
        return FileResponse(DIST_DIR / "index.html")

    # SPA 路由回退
    @app.get("/{full_path:path}")
    async def app_fallback(full_path: str):
        file_path = DIST_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(DIST_DIR / "index.html")
