from reactant.orm.django import DjangoModel, DjangoCombustor
from reactant.orm import DjangoORM
from reactant.utils import convert_to_snake
from reactant.exceptions import RenderFailed

from typing import Any, Dict, List, NamedTuple, Optional, Type, Union
from pydantic import BaseModel

from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
from black import format_str, FileMode
from click import secho


env = Environment(
    loader=PackageLoader("reactant"),
    trim_blocks=True,
)


class Reactant(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


class DjangoCombustionChamber:
    def __init__(self, reactants: List[Type[DjangoORM]]) -> None:
        self.reactants = reactants

    def _get_models(self) -> List[DjangoModel]:
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
            models = self._get_models()
            model_names = [model.name for model in models]

            self._render_models(models)
            self._render_views(model_names)
            self._render_serializers(models, model_names)
            self._render_urls(model_names)
        except Exception:
            raise

    def _render_models(self, models: List[DjangoModel]) -> None:
        item_name = "models"
        try:
            template_models = env.get_template("django_models.txt.jinja")
            output_models = template_models.render(models=models)
            formatted_code = format_str(output_models, mode=FileMode())
            with open(f"{item_name}.py", "w") as file1:
                file1.write(formatted_code)
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            self._success_secho(item_name)

    def _render_views(self, model_names: List[str]) -> None:
        item_name = "views_class"
        try:
            template_views = env.get_template("django_views.txt.jinja")
            output_views = template_views.render(names=model_names)
            formatted_code = format_str(output_views, mode=FileMode())
            with open(f"{item_name}.py", "w") as file2:
                file2.write(formatted_code)
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            self._success_secho(item_name)

    def _render_serializers(
        self, models: List[DjangoModel], model_names: List[str]
    ) -> None:
        item_name = "serializers"
        try:
            template_serializers = env.get_template("django_serializers.txt.jinja")
            output_serializers = template_serializers.render(
                models=models, names=model_names
            )
            formatted_code = format_str(output_serializers, mode=FileMode())
            with open(f"{item_name}.py", "w") as file3:
                file3.write(formatted_code)
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            self._success_secho(item_name)

    def _render_urls(self, model_names: List[str]) -> None:
        item_name = "urls_class"
        try:
            snaked_model_names = [convert_to_snake(name) for name in model_names]
            paired_names = dict(zip(model_names, snaked_model_names))
            template_urls = env.get_template("django_urls.txt.jinja")
            output_urls = template_urls.render(names=paired_names)
            formatted_code = format_str(output_urls, mode=FileMode())
            with open(f"{item_name}.py", "w") as file3:
                file3.write(formatted_code)
        except TemplateNotFound:
            raise
        except Exception:
            raise RenderFailed(item_name)
        else:
            self._success_secho(item_name)

    def _success_secho(self, item_name: str):
        return secho(f"Django {item_name}.py finished rendering.", fg="green")


class SQLAlchemyORM:
    def __str__(self):
        return "sqlalchemy"


class PeeweeORM:
    def __str__(self):
        return "peewee"


def generate() -> None:
    """
    Deliver Reactant classes to appropriate CombustionChamber
    """
    dj_classes = [
        cls for cls in DjangoORM.__subclasses__() if issubclass(cls, Reactant)
    ]

    if dj_classes:
        secho(f"Found {len(dj_classes)} Django reactants.", fg="blue")
        dj_rxn = DjangoCombustionChamber(dj_classes)
        dj_rxn.render_manager()
    else:
        secho("No Django reactants found.", fg="blue")
