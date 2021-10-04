from datetime import date
from typing import Optional

from reactant import DjangoORM, Field, PeeweeORM, generate


class RocketEngine(DjangoORM):
    name: str = Field(max_length=32, title="engine_name")
    manufacturer: Optional[str]
    power_cycle: Optional[str] = "gas-generator"
    thrust_weight_ratio: Optional[int] = None


class LaunchVehicle(PeeweeORM):
    name: str = Field(max_length=32)
    country: str = Field("USA", max_length=32)
    status: str
    total_launches: Optional[int]
    first_flight: Optional[date]
    engine: str = Field(
        related_name="vehicle",
        foreign_key="RocketEngine",
    )


if __name__ == "__main__":
    generate()
