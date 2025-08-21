import logging
from fastapi import APIRouter, Body, Query, HTTPException
from .collection_service import CollectionService

router = APIRouter()


@router.get("/collections", summary="获取所有集合")
async def get_all_collections(
    detailed: bool = Query(
        default=False, description="是否返回详细信息， 默认否", examples=[False, True]
    )
):
    """
    获取所有集合
    """
    service = CollectionService()
    collections = await service.get_all_collection()
    if detailed:
        return {"data": collections}
    else:
        return {
            "data": [
                {
                    "name": key,
                    "description": collections[key].description,
                }
                for key in collections.keys()
            ]
        }


@router.delete("/collections/{name}", summary="删除指定集合")
async def delete_collection(name: str):
    """
    删除指定名称的集合
    """
    service = CollectionService()
    try:
        result = await service.delete_collection(name)
        return {"message": f"集合 {name} 删除成功", "result": result}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"删除集合 {name} 失败: {str(e)}")
