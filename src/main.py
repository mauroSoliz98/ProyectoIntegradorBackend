from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routers.auth_router import authRouter
from src.routers.points_router import pointRouter
from src.routers.chat_router import chatRouter

#app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()

origins = [
           "http://localhost:5173",
           "https://proyectointegradorbackend-gbuj.onrender.com"
          ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura Jinja2Templates para apuntar al directorio dist
templates = Jinja2Templates(directory="../dist")

# Monta el directorio dist para servir archivos estáticos
app.mount('/assets', StaticFiles(directory="dist/assets"), name='assets')


# Incluye los routers
app.include_router(authRouter, prefix="/api/auth")
app.include_router(pointRouter, prefix="/api/points")
app.include_router(chatRouter, prefix="/api/chat")


@app.get("/")
async def serve_react():
    #return {"message": "Hello World"}
    return HTMLResponse(open("dist/index.html").read())

@app.exception_handler(404)
async def exception_404_handler(request, exc):
    return FileResponse("dist/index.html")
'''
NOTA: PONER EL SIGUEINTE COMANDO EN RENDER
prisma && uvicorn main:app --host 0.0.0.0 --port $PORT
'''