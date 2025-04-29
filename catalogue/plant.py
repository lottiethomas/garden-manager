from sqlmodel import SQLModel, Field


class PlantBase(SQLModel):
    name: str


class Plant(PlantBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PlantPublic(PlantBase):
    id: int
