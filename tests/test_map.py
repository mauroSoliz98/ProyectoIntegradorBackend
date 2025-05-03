import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

@pytest.fixture
def insert_point():
    return {
        "latitude": -16.5000,
        "longitude": -68.1193,
        "disaster_type": "Incendio",
        "severity": "alto",
        "address": "Test Address",
        "created_by_profile_id": "4c39ad99-7682-452d-ab54-bd16d7a7c5bb"
    }

def insert_point_success(insert_point):
    mock_response = {
        "id": "mocked_point_id",
        "description": insert_point["description"],
        "latitude": insert_point["latitude"],
        "longitude": insert_point["longitude"],
        "disaster_type": insert_point["disaster_type"],
        "severity": insert_point["severity"],
        "address": insert_point["address"],
        "created_at": "2025-05-03T12:00:00Z",
        "created_by_profile_id": insert_point["created_by_profile_id"]
    }

    with patch("src.supabase.point.create_point", return_value=mock_response):
        response = client.post("/api/points/", json=insert_point)
        assert response.status_code == 201
        assert response.json() == mock_response

def test_insert_point_failure(insert_point):
    with patch("src.supabase.point.create_point", side_effect=Exception("Database error")):
        response = client.post("/api/points/", json=insert_point)
        assert response.status_code == 422