import os
import httpx
import asyncio

bgem3_url = os.getenv("BGE_M3_URL", "http://127.0.0.1:4900/ai-model-service")


async def aembed_documents(texts: list[str]) -> list[list[float]]:
    async with httpx.AsyncClient(base_url=bgem3_url) as client:
        response = await client.post(
            "/models/embedding/bge-m3/documents",
            json={"texts": texts},
        )
        response.raise_for_status()
        embeddings = response.json()
        return embeddings


async def aembed_query(query: str) -> list[float]:
    async with httpx.AsyncClient(base_url=bgem3_url) as client:
        response = await client.post(
            "/models/embedding/bge-m3/query",
            json={"text": query},
        )
        response.raise_for_status()
        embed = response.json()
        return embed


if __name__ == "__main__":
    res = asyncio.run(aembed_documents(["Hello, world!"]))
    print(res)
