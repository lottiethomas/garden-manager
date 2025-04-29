from contextlib import asynccontextmanager
from typing import Any, Annotated
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, SQLModel, Session, select
from sqlalchemy import Select

from .plant import Plant, PlantPublic

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/plants", response_model=list[PlantPublic] | PlantPublic)
def get_plants(session: SessionDep, name: str | None = None) -> Any:
    if name:
        statement: Select = select(Plant).where(Plant.name == name)
        plant = session.exec(statement).first()
        if not plant:
            raise HTTPException(status_code=404, detail=f'Plant with name {name} could not be found')
        return plant
    else:
        return session.exec(select(Plant)).all()


@app.post("/plants", response_model=PlantPublic)
def add_plant(plant: Plant, session: SessionDep) -> Plant:
    session.add(plant)
    session.commit()
    session.refresh(plant)
    return plant
