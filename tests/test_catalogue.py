import json

import pytest
from fastapi.testclient import TestClient
from catalogue import catalogue
from catalogue.plant import Plant, PlantList

client = TestClient(catalogue.app)


@pytest.fixture
def save_plants():
    clematis = Plant(name="clematis")
    rose = Plant(name="rose")
    catalogue.add_plant(clematis)
    catalogue.add_plant(rose)
    return rose, PlantList([clematis, rose])


def test_get_plants():
    response = client.get("/plants")
    assert response.status_code == 200
    assert response.json() == []


def test_get_populated_plants(save_plants):
    response = client.get("/plants")
    assert response.status_code == 200
    _, expected_plants = save_plants
    assert expected_plants.model_validate_json(response.text)


def test_get_nonexistent_plant(save_plants):
    response = client.get("/plants", params={"name": "peony"})
    assert response.status_code == 404


def test_get_existent_plant(save_plants):
    response = client.get("/plants", params={"name": "rose"})
    assert response.status_code == 200
    expected_plant, all_plants = save_plants
    assert Plant(**response.json()).name == expected_plant.name
