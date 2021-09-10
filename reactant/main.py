from reactant.orm import DjangoORM
from typing import Any, Dict, List, NamedTuple, Optional, Union
from pydantic import BaseModel
from jinja2 import Environment, PackageLoader
from black import format_str, FileMode
from click import secho
from reactant.utils import convert_to_snake


env = Environment(
    loader=PackageLoader("reactant"),
    trim_blocks=True,
)


class Reactant(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


class Combustion:
    pass


class SQLAlchemyORM:
    def __str__():
        return "sqlalchemy"


class PeeweeORM:
    def __str__():
        return "peewee"


def generate() -> None:
    """
    get Reactant subclasses,
    identify ORM,
    map Reactant/ORM subclass attributes to ORM model field types,
    render from template
    """
    # Need to store the generated models before rendering to avoid rewrites
    # that cause the "import"'s being always re-rendered and duplicated.
    dj_models = []

    # Generate models with proper field types according to ORM
    for cls in Reactant.__subclasses__():
        if issubclass(cls, DjangoORM):
            model = cls.generate_django_orm_models(cls)
            dj_models.append(model)

        if issubclass(cls, SQLAlchemyORM):
            pass

        if issubclass(cls, PeeweeORM):
            pass

    # Checks and renders
    if dj_models:
        render_django(dj_models)


def render_django(models: List[NamedTuple]) -> None:
    model_names = [model.name for model in models]

    render_dj_models(models)
    render_dj_views(model_names)
    render_dj_serializers(models, model_names)
    render_dj_urls(model_names)


def render_dj_models(models: List[NamedTuple]) -> None:
    template_models = env.get_template("django_models.txt.jinja")
    output_models = template_models.render(models=models)
    formatted_code = format_str(output_models, mode=FileMode())
    with open("models.py", "w") as file1:
        file1.write(formatted_code)
        secho("Django models.py finish rendering.", fg="green")


def render_dj_views(model_names: List[str]) -> None:
    # class-based API views.py
    template_views = env.get_template("django_views.txt.jinja")
    output_views = template_views.render(names=model_names)
    formatted_code = format_str(output_views, mode=FileMode())
    with open("views_class.py", "w") as file2:
        file2.write(formatted_code)
        secho("Django views_class.py finish rendering.", fg="green")


def render_dj_serializers(models: List[NamedTuple], model_names: List[str]) -> None:
    template_serializers = env.get_template("django_serializers.txt.jinja")
    output_serializers = template_serializers.render(models=models, names=model_names)
    formatted_code = format_str(output_serializers, mode=FileMode())
    with open("serializers.py", "w") as file3:
        file3.write(formatted_code)
        secho("Django serializers.py finish rendering.", fg="green")


def render_dj_urls(model_names: List[str]) -> None:
    # class-based urls.py
    snaked_model_names = [convert_to_snake(name) for name in model_names]
    paired_names = dict(zip(model_names, snaked_model_names))
    template_urls = env.get_template("django_urls.txt.jinja")
    output_urls = template_urls.render(names=paired_names)
    formatted_code = format_str(output_urls, mode=FileMode())
    with open("urls_class.py", "w") as file3:
        file3.write(formatted_code)
        secho("Django urls_class.py finish rendering.", fg="green")
