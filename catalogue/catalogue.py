from typing import Union, Any

from fastapi import FastAPI, HTTPException

from .plant import Plant
from uuid import uuid4, UUID

app = FastAPI()

plants: list[Plant] = []


@app.get("/plants", response_model=Union[list[Plant], Plant])
def get_plants(name: str | None = None) -> Any:
    if name:
        for plant in plants:
            if plant.name == name:
                return plant
        raise HTTPException(status_code=404, detail=f'Plant with name {name} could not be found')
    else:
        return plants


@app.post("/plants")
def add_plant(plant: Plant) -> UUID:
    plants.append(plant)
    return plant.id
