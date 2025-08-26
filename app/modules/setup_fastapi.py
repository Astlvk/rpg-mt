import uvicorn
from uvicorn.config import LOGGING_CONFIG
from dotenv import load_dotenv
from app.configs import env


def build_params(prod: bool = False):
    load_dotenv()

    params = {
        "host": "127.0.0.1",
        "port": 4902,
        "reload": True,
        "app": "app.modules.main:app",
        "log_config": LOGGING_CONFIG,
        "proxy_headers": True,
        "forwarded_allow_ips": "*",
    }

    if prod:
        env["is_prod"] = True
        params["host"] = "0.0.0.0"
        params["port"] = 4902
        params["reload"] = False

    return params


def run(prod: bool = False):
    params = build_params(prod)
    # 启动fastapi服务
    uvicorn.run(**params)


if __name__ == "__main__":
    run()
