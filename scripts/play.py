from typing import Optional
from reactant import Reactant, DjangoORM, Field, generate
from datetime import date


class RocketEngine(Reactant, DjangoORM):
    name: str = Field(max_length=32, title="engine_name")
    manufacturer: Optional[str]
    power_cycle: Optional[str] = "gas-generator"
    thrust_weight_ratio: Optional[int] = None


class LaunchVehicle(Reactant, DjangoORM):
    name: str = Field(max_length=32)
    country: str = Field("USA", max_length=32)
    status: str
    total_launches: Optional[int]
    first_flight: Optional[date]
    engine: str = Field(foreign_key="RocketEngine")


if __name__ == "__main__":
    generate()
