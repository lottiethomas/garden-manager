import uuid
from pydantic import BaseModel, UUID4, Field


class Plant(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str