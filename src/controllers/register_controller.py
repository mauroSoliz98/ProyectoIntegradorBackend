from ..config.client import supabase
from src.models.user_model import UserRegister
from fastapi import HTTPException

def register_user(user_data: UserRegister):
    try:
        # 1. Crear usuario en Supabase Auth
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })

        # La respuesta es un objeto con `.user` y `.session` (a veces `.data` si usás versiones nuevas)
        user = getattr(response, "user", None)

        if not user or not user.id:
            raise Exception("No se pudo crear el usuario en Supabase Auth")

        user_id = user.id

        # 2. Insertar en la tabla profiles
        profile_data = {
            "id": user_id,
            "username": user_data.username,
            "name": user_data.name,
            "country": user_data.country,
            "email": user_data.email
        }

        insert_response = supabase.table("profiles").insert(profile_data).execute()

        if insert_response.data is None:
            raise Exception("Error al insertar en la tabla profiles")

        return {
            "message": "Usuario registrado correctamente",
            "user_id": user_id
        }

    except Exception as e:
        return {
            "error": "Error en el registro",
            "detail": str(e)
        }
