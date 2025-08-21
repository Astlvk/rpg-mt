import logging
from fastapi import APIRouter, Body, Query, HTTPException
from .summary_repo import SummaryRepo, SummaryTenantMgt

router = APIRouter()


@router.get("/summary/tenants", summary="获取所有租户")
async def get_all_tenants():
    """
    获取所有租户
    """
    repo = SummaryTenantMgt()
    try:
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
    repo = SummaryTenantMgt()
    try:
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
    repo = SummaryTenantMgt()
    try:
        await repo.remove_tenant(tenant_name)
        return {"message": f"租户 {tenant_name} 删除成功"}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"删除租户失败: {str(e)}")
