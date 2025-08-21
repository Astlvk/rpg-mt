import logging
from fastapi import APIRouter, Body, Query, HTTPException
from .summary_repo import SummaryTenantRepo, SummaryTenantMgt
from app.schema.vector_db import RagSearchModeEnum

router = APIRouter()


@router.get("/summary/tenants", summary="获取所有租户")
async def get_all_tenants():
    """
    获取所有租户
    """
    try:
        repo = SummaryTenantMgt()
        tenants = await repo.get_tenants()
        return {"data": tenants}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"获取租户失败: {str(e)}")


@router.post("/summary/tenants", summary="新增租户")
async def create_tenant(
    tenant_name: str = Body(..., embed=True, description="租户名称")
):
    """
    新增租户
    """
    try:
        repo = SummaryTenantMgt()
        await repo.create_tenant(tenant_name)
        return {"message": f"租户 {tenant_name} 创建成功"}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"创建租户失败: {str(e)}")


@router.delete("/summary/tenants/{tenant_name}", summary="删除租户")
async def delete_tenant(tenant_name: str):
    """
    删除租户
    """
    try:
        repo = SummaryTenantMgt()
        await repo.remove_tenant(tenant_name)
        return {"message": f"租户 {tenant_name} 删除成功"}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"删除租户失败: {str(e)}")


@router.post("/summary/{tenant_name}", summary="新增摘要")
async def add_summary(
    tenant_name: str, summary: str = Body(..., embed=True, description="摘要内容")
):
    """
    新增摘要
    """
    try:
        repo = SummaryTenantRepo(tenant_name)
        result = await repo.add_summary(summary)
        return {"message": "摘要添加成功", "id": result}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"新增摘要失败: {str(e)}")


@router.delete("/summary/{tenant_name}/{summary_id}", summary="删除摘要")
async def delete_summary(tenant_name: str, summary_id: str):
    """
    删除摘要
    """
    try:
        repo = SummaryTenantRepo(tenant_name)
        await repo.delete_summary(summary_id)
        return {"message": f"摘要 {summary_id} 删除成功"}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"删除摘要失败: {str(e)}")


@router.get("/summary/{tenant_name}", summary="获取对应租户的摘要列表，limit为返回数量")
async def get_summaries(
    tenant_name: str, limit: int = Query(10, description="返回数量")
):
    """
    获取摘要
    """
    try:
        repo = SummaryTenantRepo(tenant_name)
        summaries = await repo.get_summaries(limit)
        return {"data": summaries}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"获取摘要失败: {str(e)}")


@router.get(
    "/summary/{tenant_name}/cursor",
    summary="基于游标的分页查询，cursor为游标，limit为返回数量",
)
async def get_summaries_by_cursor(
    tenant_name: str,
    cursor: str = Query(None, description="游标"),
    limit: int = Query(10, description="返回数量"),
):
    """
    基于游标的分页查询
    """
    try:
        repo = SummaryTenantRepo(tenant_name)
        res = await repo.get_summary_by_cursor(cursor=cursor, limit=limit)
        return {"data": res}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"获取摘要失败: {str(e)}")


@router.get("/summary/{tenant_name}/vector_search", summary="向量搜索摘要")
async def vector_search(
    tenant_name: str,
    query: str = Query(..., embed=True, description="查询内容"),
    mode: RagSearchModeEnum = Query(
        RagSearchModeEnum.similarity, description="搜索模式 similarity/hybrid"
    ),
    distance: float = Query(0.5, description="相似度距离"),
    k: int = Query(5, description="返回数量"),
):
    """
    RAG搜索摘要
    """
    try:
        repo = SummaryTenantRepo(tenant_name)
        results = await repo.vector_search(
            query=query, mode=mode, distance=distance, k=k
        )
        return {"data": results}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"RAG搜索失败: {str(e)}")
