import logging
from fastapi import APIRouter, Body, Request, HTTPException
from app.ai_models.embeddings import aembed_documents, aembed_query

router = APIRouter()


@router.post("/embed/documents", summary="批量文本转向量")
async def embed_documents(
    texts: list[str] = Body(..., examples=[["你好", "世界"]], embed=True)
):
    """
    批量将文本转为向量
    """
    if not texts or not isinstance(texts, list):
        raise HTTPException(status_code=400, detail="参数 texts 必须为字符串列表")
    try:
        embeddings = await aembed_documents(texts)
        return embeddings
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"向量化失败: {str(e)}")


@router.post("/embed/query", summary="查询文本转向量")
async def embed_query(text: str = Body(..., examples=["你好世界"], embed=True)):
    """
    将查询文本转为向量
    """
    if not text or not isinstance(text, str):
        raise HTTPException(status_code=400, detail="参数 text 必须为字符串")
    try:
        embedding = await aembed_query(text)
        return embedding
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"向量化失败: {str(e)}")
