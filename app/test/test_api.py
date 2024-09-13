import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from auth.dependencies import get_current_user, get_current_user_dummy
from air_pollution.router import app as air_pollution_router


app = FastAPI()
app.include_router(air_pollution_router)

client = TestClient(app)


# Use the override during tests
app.dependency_overrides[get_current_user] = get_current_user_dummy

def test_api_status():
    response = client.get("/docs")
    assert response.status_code == 200


def test_read_protected_data():
    response = client.get("/pollution_data/get?country=Germany&year=2018")
    assert response.status_code == 200
    assert (response.json()["Mean"] > 12.5) and (response.json()["Mean"] < 12.6) 


def test_api_error():
    response = client.get("/pollution_data/get?country=Afghanistan&year=2010")
    assert response.status_code == 404

# def test_api_count():
#     # anzahl der datenpunkte
#     pass

# def test_api_auth():
#     pass