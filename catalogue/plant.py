import uuid
from typing import List

from pydantic import BaseModel, UUID4, Field, RootModel


class Plant(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str


class PlantList(RootModel[List[Plant]]):
    def __init__(self, plants: List[Plant]):
        super().__init__(plants)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
