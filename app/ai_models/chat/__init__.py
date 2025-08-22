from langchain_core.language_models import BaseChatModel
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


def get_chat_model(model: str, api_key: str, base_url: str, **kwargs):
    chat_model = init_chat_model(
        model=model,
        model_provider="openai",
        base_url=base_url,
        configurable_fields=("api_key", api_key),
        **kwargs,
    )
    return chat_model


if __name__ == "__main__":
    load_dotenv()
    # model = get_chat_model("glm-4.5-flash")
    # response = model.invoke("你好")
    # print(response)
