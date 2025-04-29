import pytest
from fastapi.testclient import TestClient
from pydantic import TypeAdapter
from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool
from catalogue import catalogue
from catalogue.plant import Plant


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    catalogue.app.dependency_overrides[catalogue.get_session] = get_session_override

    client = TestClient(catalogue.app)
    yield client
    catalogue.app.dependency_overrides.clear()


@pytest.fixture
def save_plants(session: Session):
    rose = Plant(name="rose")
    clematis = Plant(name="clematis")
    session.add(rose)
    session.add(clematis)
    session.commit()
    return rose, [rose, clematis]


def test_get_plants(client: TestClient):
    response = client.get("/plants")
    assert response.status_code == 200
    assert response.json() == []


def test_get_populated_plants(client: TestClient, save_plants):
    response = client.get("/plants")
    assert response.status_code == 200
    _, expected_plants = save_plants
    plant_list_adapter = TypeAdapter(list[Plant])
    received_list = plant_list_adapter.validate_python(response.json())
    assert expected_plants == received_list


def test_get_nonexistent_plant(client: TestClient, save_plants):
    response = client.get("/plants", params={"name": "peony"})
    assert response.status_code == 404


def test_get_existent_plant(client: TestClient, save_plants):
    response = client.get("/plants", params={"name": "rose"})
    assert response.status_code == 200
    expected_plant, all_plants = save_plants
    assert Plant(**response.json()).name == expected_plant.name
