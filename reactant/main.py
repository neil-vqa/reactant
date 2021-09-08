from typing import Any, Dict, List, Optional, Union
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


class AlchemyORM:
    def __str__():
        return "sqlalchemy"


class PeeweeORM:
    def __str__():
        return "peewee"


class ReactantColumn:
    def __init__(
        self, name: str, column_type: str, options: List[Dict[str, Any]]
    ) -> None:
        self.name = name
        self.column_type = column_type
        self.options = options


class ReactantFieldInfo(FieldInfo):
    def __init__(self, default: Any, **kwargs: Any) -> None:
        self.primary_key = kwargs.pop("primary_key", False)
        self.unique = kwargs.pop("unique", False)
        self.nullable = kwargs.pop("nullable", False)
        self.blank = kwargs.pop("blank", False)
        self.min_length = kwargs.pop("min_length", None)
        self.max_length = kwargs.pop("max_length", None)
        self.max_digits = kwargs.pop("max_digits", None)
        self.decimal_places = kwargs.pop("decimal_places", None)
        super().__init__(default=default, **kwargs)


def Field(
    default: Any = Undefined,
    primary_key=None,
    unique=None,
    nullable=None,
    blank=None,
    min_length=None,
    max_length=None,
    max_digits=None,
    decimal_places=None,
) -> Any:
    field_info = ReactantFieldInfo(
        default=default,
        primary_key=primary_key,
        unique=unique,
        nullable=nullable,
        blank=blank,
        min_length=min_length,
        max_length=max_length,
        max_digits=max_digits,
        decimal_places=decimal_places,
    )
    return field_info


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
