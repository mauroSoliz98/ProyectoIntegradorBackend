from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routers.auth_router import authRouter
from src.routers.points_router import pointRouter
from src.routers.chat_router import chatRouter

app = FastAPI()

origins = [
           "http://localhost:5173",
           "https://integrador-front-mau.netlify.app",
           "http://localhost:4173"
          ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye los routers
app.include_router(authRouter, prefix="/api/auth")
app.include_router(pointRouter, prefix="/api/points")
app.include_router(chatRouter, prefix="/api/chat")  # Esto ya incluye el WebSocket en /api/chat/ws

@app.get("/")
async def serve_react():
    return {"message": "Hello World"}

# Endpoint de prueba para verificar que el servidor está funcionando
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running"}