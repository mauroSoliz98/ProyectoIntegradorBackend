import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

@pytest.fixture
def valid_credentials():
    return {
        "username": "admin2025",
        "password": "admin123"
    }

def test_login_success(valid_credentials):
    mock_user = MagicMock()
    mock_user.id = "mocked_user_id"
    mock_user.email = "pytestUser@example.com"

    profile_data = [{
        "id": "mocked_profile_id",
        "email": mock_user.email,
        "name": "Test User",
        "country": "Bolivia",
        "username": valid_credentials["username"]
    }]

    with patch("src.controllers.login_controller.supabase") as mock_supabase:
        # Mock profile lookup
        mock_query = MagicMock()
        mock_query.select.return_value.eq.return_value.execute.return_value.data = profile_data
        mock_supabase.table.return_value = mock_query

        # Mock auth
        mock_supabase.auth.sign_in_with_password.return_value.user = mock_user

        response = client.post("/api/auth/login", json=valid_credentials)
        assert response.status_code == 200
        assert "user_id" in response.json()
        assert response.json()["email"] == mock_user.email

def test_login_invalid_credentials(valid_credentials):
    with patch("src.controllers.login_controller.supabase") as mock_supabase:
        # Simular perfil encontrado
        mock_query = MagicMock()
        mock_query.select.return_value.eq.return_value.execute.return_value.data = [{
            "id": "mocked_id",
            "email": "pytestUser@example.com",
            "name": "Test User",
            "country": "Bolivia",
            "username": valid_credentials["username"]
        }]
        mock_supabase.table.return_value = mock_query

        # Simular login fallido (contraseña incorrecta)
        mock_supabase.auth.sign_in_with_password.return_value.user = None

        response = client.post("/api/auth/login", json=valid_credentials)
        assert response.status_code == 401
        assert "Contraseña incorrecta" in response.text

def test_login_invalid_username_format():
    invalid_data = {
        "username": 1234,  # username debe ser string
        "password": "somepassword"
    }

    response = client.post("/api/auth/login", json=invalid_data)
    assert response.status_code == 422  # Error de validación FastAPI
