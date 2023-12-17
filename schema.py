from abc import ABC
from typing import Optional

import pydantic


class AbstractAdvt(pydantic.BaseModel, ABC):
    title: str
    description: str
    owner: str

    @pydantic.field_validator("title")
    @classmethod
    def length_title(cls, v: str) -> str:
        if len(v) <= 1 or len(v) > 50:
            raise ValueError(f"Minimum length of title is 2, maximum 50")
        return v


class CreateAdvt(AbstractAdvt):
    title: str
    description: str
    owner: str


class UpdateAdvt(AbstractAdvt):
    title: Optional[str]
    description: Optional[str]
    owner: Optional[str]
