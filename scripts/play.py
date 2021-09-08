from typing import Optional
from reactant import Reactant, DjangoORM, generate


class Airplane(Reactant, DjangoORM):
    id: int
    name: str
    company: str = "Lockheed"
    operator: Optional[str]


class Ship(Reactant, DjangoORM):
    id: int
    name: str
    company: str = "Cockaliong"


if __name__ == "__main__":
    generate()
