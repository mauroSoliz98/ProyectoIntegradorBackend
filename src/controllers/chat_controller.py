import uuid
from ..config.client import supabase
from datetime import datetime, timezone
from src.models.chat_model import CreateMessage, ResponseMessage
from fastapi import HTTPException

def get_messages(profile_id: str) -> list[ResponseMessage]:
    try:
        response = supabase.table("messages").select("*").eq("profile_id", profile_id).execute()
        data = response.data or []
        return [ResponseMessage(**message) for message in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

def create_message(message_data: CreateMessage) -> ResponseMessage:
    try:
        new_id = str(uuid.uuid4())
        
        # Datos a insertar
        insert_data = {
            "id": new_id,
            "profile_id": message_data.profile_id,
            "content": message_data.content,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        print(f"Insertando datos: {insert_data}")  # Debug
        
        response = supabase.table("messages").insert(insert_data).execute()
        
        print(f"Respuesta de Supabase: {response}")  # Debug
        
        # Verificar si hay datos en la respuesta
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=500, detail="No se pudo crear el mensaje")
        
        # Retornar el mensaje creado
        created_message = response.data[0]
        return ResponseMessage(**created_message)
        
    except Exception as e:
        print(f"Error en create_message: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=f"Error al crear el mensaje: {str(e)}")
