from typing import Any
from langchain.chat_models import BaseChatModel, init_chat_model
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
    # model = get_chat_model("gpt-4.1-mini", api_key="...", base_url="https://api.openai.com/v1")
    # response = model.invoke("你好")
    # print(response)
