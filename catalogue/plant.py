import uuid
from typing import List, Iterator

from pydantic import BaseModel, UUID4, Field, RootModel


class Plant(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str


class PlantList(RootModel[List[Plant]]):
    def __init__(self, plants: List[Plant]):
        super().__init__(plants)

    def __iter__(self) -> Iterator[Plant]:
        return iter(self.root)

    def __getitem__(self, item) -> Plant:
        return self.root[item]

    def append(self, item) -> None:
        self.root.append(item)
