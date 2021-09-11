from typing import Optional
from reactant import Reactant, DjangoORM, Field, generate


class RocketEngine(Reactant, DjangoORM):
    id: int = Field(primary_key=True, title="rocket_id")
    name: str = Field(max_length=32)
    manufacturer: str = Field(max_length=64)
    power_cycle: Optional[str] = Field(
        "gas-generator", nullable=True, blank=True, max_length=32
    )
    thrust_weight_ratio: int


class LaunchVehicle(Reactant, DjangoORM):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=32)
    country: str = Field(blank=True, max_length=32)


if __name__ == "__main__":
    generate()
