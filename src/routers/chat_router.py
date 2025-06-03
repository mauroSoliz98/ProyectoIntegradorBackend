from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List
from src.models.chat_model import CreateMessage, ResponseMessage
from src.controllers.chat_controller import create_message, get_messages

chatRouter = APIRouter()
active_connections: List[WebSocket] = []

# Endpoint HTTP para testing con Postman
@chatRouter.post("/messages", response_model=ResponseMessage)
async def create_message_http(message_data: CreateMessage):
    """Endpoint HTTP para crear mensajes - útil para testing con Postman"""
    try:
        result = create_message(message_data)
        
        # Notificar a las conexiones WebSocket activas
        if active_connections:
            for connection in active_connections:
                try:
                    await connection.send_json(result.model_dump())
                except:
                    # Remover conexiones cerradas
                    active_connections.remove(connection)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener mensajes
@chatRouter.get("/messages/{profile_id}", response_model=List[ResponseMessage])
async def get_messages_http(profile_id: str):
    """Endpoint para obtener mensajes de un perfil"""
    return get_messages(profile_id)

# WebSocket para chat en tiempo real
@chatRouter.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()  # Cambiar a receive_json
            
            # Esperamos recibir un objeto con profile_id y content
            if isinstance(data, dict):
                message_data = CreateMessage(**data)
            else:
                # Si es solo texto, usar profile_id por defecto
                message_data = CreateMessage(
                    content=str(data), 
                    profile_id="default_profile_id"
                )
            
            response_message = create_message(message_data)
            
            # Enviar a todas las conexiones activas
            for connection in active_connections:
                try:
                    await connection.send_json(response_message.model_dump())
                except:
                    # Remover conexiones cerradas
                    if connection in active_connections:
                        active_connections.remove(connection)
                        
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        await websocket.close(code=1000, reason=str(e))
        if websocket in active_connections:
            active_connections.remove(websocket)
