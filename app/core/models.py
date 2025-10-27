from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ReplayData(BaseModel):
    model_config = ConfigDict(extra="allow")

    conceal: bool = Field(...)
    date: str = Field(...)
    plays: list[dict[str, Any]] = Field(...)
