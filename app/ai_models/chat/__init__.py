from typing import Any
from langchain.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


def get_chat_model(
    model: str, api_key: str, base_url: str, **kwargs: Any
) -> BaseChatModel:
    model_provider = "deepseek" if "deepseek" in model else "openai"

    chat_model = init_chat_model(
        model=model,
        model_provider=model_provider,
        base_url=base_url,
        api_key=api_key,
        **kwargs,
    )
    return chat_model


if __name__ == "__main__":
    load_dotenv()
    # model = get_chat_model("glm-4.5-flash")
    # response = model.invoke("你好")
    # print(response)
