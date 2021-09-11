from reactant import __version__, Reactant, DjangoORM, Field, generate
from typing import Optional
from pathlib import Path


def test_version():
    assert __version__ == "0.1.0"


def test_generate_django_files_success():
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

    generate()

    models = Path("models.py")
    views_class = Path("views_class.py")
    serializers = Path("serializers.py")
    urls_class = Path("urls_class.py")

    assert models.is_file()
    assert views_class.is_file()
    assert serializers.is_file()
    assert urls_class.is_file()
