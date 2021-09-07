from typing import Any
from pydantic import BaseModel


class Reactant(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

    def annotations(__pydantic_self__):
        return __pydantic_self__.__annotations__


def create_all():
    [print((cls.__name__, cls.__annotations__)) for cls in Reactant.__subclasses__()]
