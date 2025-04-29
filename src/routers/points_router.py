from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from src.models.point_model import RequestPoint, ResponsePoint
from src.supabase.point import get_points, create_point, delete_point, update_point

pointRouter = APIRouter()

@pointRouter.get("/", response_model=List[ResponsePoint])
async def read_points():
    try:
        return get_points()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@pointRouter.post("/", response_model=ResponsePoint, status_code=status.HTTP_201_CREATED)
async def add_point(payload: RequestPoint):
    try:
        return create_point(payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@pointRouter.delete("/{point_id}")
async def remove_point(point_id: UUID):
    try:
        delete_point(point_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@pointRouter.put("/{point_id}", response_model=ResponsePoint)
async def alter_point(point_id: UUID, payload: RequestPoint):
    try:
        return update_point(point_id, payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))