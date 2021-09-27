from reactant.orm.django import DjangoModel
from reactant.orm.peewee import PeeweeModel
from reactant.renderer.django import DjangoCombustionChamber
from reactant.renderer.peewee import PeeweeCombustionChamber
from reactant import __version__, DjangoORM, Field, generate, PeeweeORM
from typing import Optional
from pathlib import Path


def test_version():
    assert __version__ == "0.3.1"


class TestDjango:
    def test_django_combustion_chamber_get_models_method_return_djangomodels(self):
        class RocketEngine(DjangoORM):
            id: int = Field(primary_key=True, title="rocket_id")
            name: str = Field(max_length=32)
            manufacturer: str = Field(max_length=64)
            power_cycle: Optional[str] = Field(
                "gas-generator", nullable=True, blank=True, max_length=32
            )
            thrust_weight_ratio: int

        combust = DjangoCombustionChamber([RocketEngine])
        models = combust.get_models()

        assert isinstance(models, list)
        assert isinstance(models[0], DjangoModel)

    def test_generate_django_files_success(self):
        class RocketEngine(DjangoORM):
            id: int = Field(primary_key=True, title="rocket_id")
            name: str = Field(max_length=32)
            manufacturer: str = Field(max_length=64)
            power_cycle: Optional[str] = Field(
                "gas-generator", nullable=True, blank=True, max_length=32
            )
            thrust_weight_ratio: int

        generate()

        p = "reactant_products/django"
        dj_models = Path(f"{p}/models.py")
        dj_views_class = Path(f"{p}/views_class.py")
        dj_serializers = Path(f"{p}/serializers.py")
        dj_urls_class = Path(f"{p}/urls_class.py")

        assert dj_models.is_file()
        assert dj_views_class.is_file()
        assert dj_serializers.is_file()
        assert dj_urls_class.is_file()

        dj_models.unlink()
        dj_views_class.unlink()
        dj_serializers.unlink()
        dj_urls_class.unlink()


class TestPeewee:
    def test_peewee_combustion_chamber_get_models_method_return_peeweemodels(self):
        class RocketEngine(PeeweeORM):
            id: int = Field(primary_key=True, title="rocket_id")
            name: str = Field(max_length=32)
            manufacturer: str = Field(max_length=64)
            power_cycle: Optional[str] = Field(
                "gas-generator", nullable=True, blank=True, max_length=32
            )
            thrust_weight_ratio: int

        combust = PeeweeCombustionChamber([RocketEngine])
        models = combust.get_models()

        assert isinstance(models, list)
        assert isinstance(models[0], PeeweeModel)

    def test_generate_peewee_files_success(self):
        class RocketEngine(PeeweeORM):
            id: int = Field(primary_key=True, title="rocket_id")
            name: str = Field(max_length=32)
            manufacturer: str = Field(max_length=64)
            power_cycle: Optional[str] = Field(
                "gas-generator", nullable=True, blank=True, max_length=32
            )
            thrust_weight_ratio: int

        generate()

        p = "reactant_products/peewee"
        models = Path(f"{p}/models.py")

        assert models.is_file()

        models.unlink()
