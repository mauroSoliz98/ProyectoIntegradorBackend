from typing import List
from uuid import UUID
from datetime import datetime, timezone
from .client import supabase
from src.models.point_model import RequestPoint, ResponsePoint

TABLE = "points_of_interest"

def get_points() -> List[ResponsePoint]:
        response = supabase.table(TABLE).select("*").execute()
        data = response.data or []
        return [ResponsePoint(**point) for point in data]


def create_point(point: RequestPoint) -> ResponsePoint:
    payload = point.model_dump()
    # Convertir UUID a str para JSON
    payload["created_by_profile_id"] = str(payload["created_by_profile_id"])
    # Asignamos timestamp ISO con zona UTC
    payload["created_at"] = datetime.now(timezone.utc).isoformat()
    # created_by_profile_id ya está en payload
    response = supabase.table(TABLE).insert(payload).execute()
    item = response.data[0]
    return ResponsePoint(**item)

def delete_point(point_id: UUID):
        respose = supabase.table(TABLE).delete().eq("id", str(point_id)).execute()
        return {"message": "Point with id {point_id} deleted successfully."} 

def update_point(point_id: UUID, point: RequestPoint) -> ResponsePoint:
        updates = point.model_dump(exclude_unset=True)
        # Convertir UUID a str si está presente
        if "created_by_profile_id" in updates:
                updates["created_by_profile_id"] = str(updates["created_by_profile_id"])
        response = (
                supabase.table(TABLE)
                .update(updates)
                .eq("id", str(point_id))
                .execute()
        )
        item = response.data[0]
        return ResponsePoint(**item)