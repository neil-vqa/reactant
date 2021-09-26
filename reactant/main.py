from reactant.orm.django import DjangoModel, DjangoCombustor
from reactant.orm.peewee import PeeweeModel, PeeweeCombustor
from reactant.utils import convert_to_snake
from reactant.exceptions import RenderFailed

from typing import (
    Any,
    Iterable,
    List,
    Tuple,
    Type,
)
from pydantic import BaseModel

from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
from black import format_str, FileMode
from click import secho
from pathlib import Path


env = Environment(
    loader=PackageLoader("reactant"),
    trim_blocks=True,
)


class Reactant(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


class DjangoORM(Reactant):
    def __str__(self):
        return "django"


class PeeweeORM(Reactant):
    def __str__(self):
        return "peewee"


class SQLAlchemyORM(Reactant):
    def __str__(self):
        return "sqlalchemy"


class DjangoCombustionChamber:
    """For rendering Reactant models that are DjangoORM subclasses."""

    def __init__(self, reactants: List[Type[DjangoORM]]) -> None:
        self.reactants = reactants

    def get_models(self) -> List[DjangoModel]:
        models = []
        for reactant in self.reactants:
            try:
                model = DjangoCombustor.generate_django_orm_model(reactant)
                models.append(model)
            except Exception:
                raise
        return models

    def render_manager(self) -> None:
        try:
            models = self.get_models()
            model_names = [model.name for model in models]

            models_code, models_name_str = self.render_models(models)
            views_code, views_name_str = self.render_views(model_names)
            serializers_code, serializers_name_str = self.render_serializers(
                models, model_names
            )
            urls_code, urls_name_str = self.render_urls(model_names)

            self.write_to_file(models_code, models_name_str)
            self.write_to_file(views_code, views_name_str)
            self.write_to_file(serializers_code, serializers_name_str)
            self.write_to_file(urls_code, urls_name_str)
        except Exception:
            raise

    def render_models(self, models: List[DjangoModel]) -> Tuple[str, str]:
        item_name = "models"
        try:
            template_models = env.get_template("django_models.txt.jinja")
            output_models = template_models.render(models=models)
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_models, item_name)

    def render_views(self, model_names: List[str]) -> Tuple[str, str]:
        item_name = "views_class"
        try:
            template_views = env.get_template("django_views.txt.jinja")
            output_views = template_views.render(names=model_names)
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_views, item_name)

    def render_serializers(
        self, models: List[DjangoModel], model_names: List[str]
    ) -> Tuple[str, str]:
        item_name = "serializers"
        try:
            template_serializers = env.get_template("django_serializers.txt.jinja")
            output_serializers = template_serializers.render(
                models=models, names=model_names
            )
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_serializers, item_name)

    def render_urls(self, model_names: List[str]) -> Tuple[str, str]:
        item_name = "urls_class"
        try:
            snaked_model_names = [convert_to_snake(name) for name in model_names]
            paired_names = dict(zip(model_names, snaked_model_names))
            template_urls = env.get_template("django_urls.txt.jinja")
            output_urls = template_urls.render(names=paired_names)
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_urls, item_name)

    def write_to_file(self, item: Any, item_name: str) -> None:
        try:
            p = Path("reactant_products/django")
            p.mkdir(parents=True, exist_ok=True)
            formatted_code = format_str(item, mode=FileMode())
            with open(f"{p}/{item_name}.py", "w") as file:
                file.write(formatted_code)
        except Exception:
            raise
        else:
            self._success_secho(item_name)

    def _success_secho(self, item_name: str):
        return secho(f"Django {item_name}.py finished rendering.", fg="green")


class PeeweeCombustionChamber:
    """For rendering Reactant models that are PeeweeORM subclasses."""

    def __init__(self, reactants: List[Type[PeeweeORM]]) -> None:
        self.reactants = reactants

    def get_models(self) -> List[PeeweeModel]:
        models = []
        for reactant in self.reactants:
            try:
                model = PeeweeCombustor.generate_peewee_orm_model(reactant)
                models.append(model)
            except Exception:
                raise
        return models

    def render_manager(self) -> None:
        try:
            models = self.get_models()
            fields_list = []
            for model in models:
                for field in model.fields:
                    fields_list.append(field.type)
            fields_set = set(fields_list)
            models_code, models_name_str = self.render_models(models, fields_set)
            self.write_to_file(models_code, models_name_str)
        except Exception:
            raise

    def render_models(
        self, models: List[PeeweeModel], fields_set: Iterable
    ) -> Tuple[str, str]:
        item_name = "models"
        try:
            template_models = env.get_template("peewee_models.txt.jinja")
            output_models = template_models.render(models=models, fields_set=fields_set)
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_models, item_name)

    def write_to_file(self, item: Any, item_name: str) -> None:
        try:
            p = Path("reactant_products/peewee")
            p.mkdir(parents=True, exist_ok=True)
            formatted_code = format_str(item, mode=FileMode())
            with open(f"{p}/{item_name}.py", "w") as file:
                file.write(formatted_code)
        except Exception:
            raise
        else:
            self._success_secho(item_name)

    def _success_secho(self, item_name: str):
        return secho(f"Peewee {item_name}.py finished rendering.", fg="green")


def classify_reactants() -> Tuple[List[Any], ...]:
    dj_classes = [cls for cls in DjangoORM.__subclasses__()]
    alchemy_classes = [cls for cls in SQLAlchemyORM.__subclasses__()]
    peewee_classes = [cls for cls in PeeweeORM.__subclasses__()]

    return (dj_classes, alchemy_classes, peewee_classes)


def generate() -> None:
    """
    Deliver Reactant models to appropriate CombustionChamber.
    CombustionChamber classes contain methods for rendering specific files
    according to the selected Reactant subclass.
    """

    dj_classes, alchemy_classes, peewee_classes = classify_reactants()

    if dj_classes:
        secho(f"Found {len(dj_classes)} Django reactants.", fg="blue")
        dj_rxn = DjangoCombustionChamber(dj_classes)
        dj_rxn.render_manager()
    else:
        secho("No Django reactants found.", fg="blue")

    if peewee_classes:
        secho(f"Found {len(peewee_classes)} Peewee reactants.", fg="blue")
        pw_rxn = PeeweeCombustionChamber(peewee_classes)
        pw_rxn.render_manager()
    else:
        secho("No Peewee reactants found.", fg="blue")
