from fastapi import APIRouter, HTTPException
from src.models.user_model import UserRegister
from src.models.user_model import UserLogin
from src.controllers.register_controller import register_user
from src.controllers.login_controller import login_user

authRouter = APIRouter(tags=["Auth"])

@authRouter.post("/register")
def register(user_data: UserRegister):
    response = register_user(user_data)
    
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["detail"])
    
    return response

@authRouter.post("/login")
def login(user_data: UserLogin):
    response = login_user(user_data)
    
    if "error" in response:
        raise HTTPException(status_code=401, detail=response["detail"])
    
    return response