from ..config.client import supabase
from src.models.user_model import UserLogin
from fastapi import HTTPException

def login_user(user_data: UserLogin):
    try:
        # Buscar el perfil por username
        profile_response = (
            supabase.table("profiles")
            .select("id, email, name, country, username")
            .eq("username", user_data.username)
            .execute()
        )

        if not profile_response.data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        profile = profile_response.data[0]
        email = profile["email"]

        # Iniciar sesión con email y password
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": user_data.password
        })

        if auth_response.user is None:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        return {
            "user_id": auth_response.user.id,
            "email": auth_response.user.email,
            "profile": profile
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
