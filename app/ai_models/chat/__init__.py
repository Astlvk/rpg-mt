from langchain_core.language_models import BaseChatModel
from langchain_google_genai import HarmBlockThreshold, HarmCategory
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from app.schema.models_enum import GeminiModelEnum


def get_chat_model(model: str, api_key: str, base_url: str, **kwargs):
    model_provider = "openai"
    # if model in [item.value for item in GeminiModelEnum]:
    #     model_provider = "google_genai"

    # print("model_provider================================", model_provider)

    chat_model = init_chat_model(
        model=model,
        model_provider=model_provider,
        base_url=base_url,
        api_key=api_key,
        configurable_fields=("api_key", api_key),
        # safety_settings={
        #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.OFF,
        #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.OFF,
        #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.OFF,
        #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.OFF,
        #     HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.OFF,
        # },
        **kwargs,
    )
    return chat_model


if __name__ == "__main__":
    load_dotenv()
    # model = get_chat_model("glm-4.5-flash")
    # response = model.invoke("你好")
    # print(response)
