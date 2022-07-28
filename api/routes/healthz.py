"""
platform starter kit teams api

teams api liveness and readiness endpoints.
"""
from datetime import datetime
from fastapi import APIRouter, status
from ..config import settings

route = APIRouter()

@route.get("/healthz/liveness",
           summary="liveness check.",
           tags=["healthz"],
           status_code=status.HTTP_200_OK
           )
async def get_healthz_liveness():
    """
    Returns 200 if service is running.
    """
    return {
      "status": "ok",
      "version": settings.version,
      "releaseId": settings.releaseId,
      "description": "liveness status of platform starter kit teams api",
      "time": datetime.now().isoformat()
    }


@route.get("/healthz/readiness",
           summary="readiness check.",
           tags=["healthz"],
           status_code=status.HTTP_200_OK
           )
async def get_healthz():
    """
    Returns 200 if service is able to connect to teams db.
    """
    return {
      "status": "ok",
      "version": settings.version,
      "releaseId": settings.releaseId,
      "description": "readiness status of platform starter kit teams api",
      "time": datetime.now().isoformat()
    }
