from typing import Optional
from reactant import Reactant, DjangoORM, Field, generate


class RocketEngine(Reactant, DjangoORM):
    name: str = Field(max_length=32, title="engine_name")
    manufacturer: str = Field(max_length=64)
    power_cycle: Optional[str] = Field("gas-generator", blank=True, max_length=32)
    thrust_weight_ratio: Optional[int] = None


class LaunchVehicle(Reactant, DjangoORM):
    name: str = Field(max_length=32)
    country: str = Field(blank=True, max_length=32)
    status: str


if __name__ == "__main__":
    generate()
