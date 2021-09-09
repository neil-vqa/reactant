from typing import Any, Dict, List, NamedTuple, Optional, Union
from pydantic import BaseModel
from pydantic.fields import Undefined, FieldInfo, UndefinedType
from jinja2 import Environment, PackageLoader
from yapf.yapflib.yapf_api import FormatCode


env = Environment(
    loader=PackageLoader("reactant"),
    trim_blocks=True,
)


class Reactant(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


class DjangoORM:
    def __str__():
        return "django"


class SQLAlchemyORM:
    def __str__():
        return "sqlalchemy"


class PeeweeORM:
    def __str__():
        return "peewee"


def generate():
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
            from reactant.orm import generate_django_orm_models

            model = generate_django_orm_models(cls)
            dj_models.append(model)

        if issubclass(cls, SQLAlchemyORM):
            pass

        if issubclass(cls, PeeweeORM):
            pass

    # Checks and renders
    if dj_models:
        render_django(dj_models)


def render_django(models: List[NamedTuple]):
    model_names = [model.name for model in models]

    # render models.py
    template_models = env.get_template("django_models.txt.jinja")
    output_models = template_models.render(models=models)
    formatted_code, _ = FormatCode(output_models)
    with open("models.py", "w") as file1:
        file1.write(formatted_code)
        print("Django models.py finish rendering.")

    # render class-based API views.py
    template_views = env.get_template("django_views.txt.jinja")
    output_views = template_views.render(names=model_names)
    formatted_code, _ = FormatCode(output_views)
    with open("views_class.py", "w") as file2:
        file2.write(formatted_code)
        print("Django views_class.py finish rendering.")

    # render serializers.py
    template_serializers = env.get_template("django_serializers.txt.jinja")
    output_serializers = template_serializers.render(models=models, names=model_names)
    formatted_code, _ = FormatCode(output_serializers)
    with open("serializers.py", "w") as file3:
        file3.write(formatted_code)
        print("Django serializers.py finish rendering.")
