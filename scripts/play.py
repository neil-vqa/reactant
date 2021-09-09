from typing import Optional
from reactant import Reactant, DjangoORM, generate, Field


class Airplane(Reactant, DjangoORM):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=64)
    company: str = "Lockheed"
    operator: Optional[str] = Field(nullable=True, blank=True)


class Spaceship(Reactant, DjangoORM):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=64)
    company: str = "SpaceX"


if __name__ == "__main__":
    generate()
