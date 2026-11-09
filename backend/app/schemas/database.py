
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DatabaseCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=63,
        pattern=r"^[a-z][a-z0-9_]*$",
    )

    engine: str = Field(default="postgresql")
    version: str = Field(default="16")

    storage_mb: int = Field(
        default=1024,
        gt=0,
        le=102400,
    )

    max_connections: int = Field(
        default=20,
        gt=0,
        le=100,
    )


class DatabaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    engine: str
    version: str
    status: str
    storage_mb: int
    max_connections: int
    owner_id: uuid.UUID
    created_at: datetime
