from typing import Any
from pydantic import BaseModel
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


class AlchemyORM:
    def __str__():
        return "sqlalchemy"


class PeeweeORM:
    def __str__():
        return "peewee"


def generate():
    """
    get Reactant subclass,
    identify ORM,
    map Reactant subclass attributes to ORM model types,
    create ORM model,
    build template
    """
    dj_models = []

    for cls in Reactant.__subclasses__():
        if issubclass(cls, DjangoORM):
            from reactant.orm import generate_django_orm_models

            model = generate_django_orm_models(cls)
            dj_models.append(model)

        elif issubclass(cls, AlchemyORM):
            pass

        elif issubclass(cls, PeeweeORM):
            pass

    if dj_models:
        template = env.get_template("django_models.txt.jinja")
        output = template.render(models=dj_models)
        formatted_code, _ = FormatCode(output)
        with open("models.py", "w") as f:
            f.write(formatted_code)
