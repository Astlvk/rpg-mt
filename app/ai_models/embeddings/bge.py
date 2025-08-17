import asyncio
from langchain_huggingface import HuggingFaceEmbeddings
from app.configs.embedding import bgem3


model_bgem3: HuggingFaceEmbeddings | None = None


def init_model():
    model_name = bgem3.get("model_name")
    model_kwargs = bgem3.get("model_kwargs")
    encode_kwargs = bgem3.get("encode_kwargs")
    global model_bgem3
    model_bgem3 = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )


def get_model():
    if model_bgem3 is None:
        raise RuntimeError("Model not initialized. Call init_model() first.")
    return model_bgem3


async def aembed_documents(texts: list[str]) -> list[list[float]]:
    model = get_model()
    embeddings = await model.aembed_documents(texts)
    print(len(embeddings))
    return embeddings


async def aembed_query(query: str) -> list[float]:
    model = get_model()
    embed = await model.aembed_query(query)
    return embed


if __name__ == "__main__":
    asyncio.run(aembed_documents(["Hello, world!"]))
