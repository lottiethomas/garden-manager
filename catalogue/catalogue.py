from typing import Any

from fastapi import FastAPI, HTTPException

from .plant import Plant, PlantList
from uuid import UUID

app = FastAPI()

plants: PlantList = PlantList([])


@app.get("/plants", response_model=PlantList | Plant)
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
