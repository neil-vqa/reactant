import ipaddress
import uuid

from typing import Any, Dict, NamedTuple, List, Type
from pydantic.fields import ModelField, UndefinedType

from datetime import date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from django.db.models import (
    BinaryField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    DurationField,
    FloatField,
    GenericIPAddressField,
    IntegerField,
    TimeField,
    UUIDField,
)


class DjangoORM:
    def __str__(self):
        return "django"


class FieldOptions(NamedTuple):
    name: str
    type: str
    extras: Dict[Any, Any]


class DjangoModel(NamedTuple):
    name: str
    fields: List[FieldOptions]


class DjangoCombustor:
    @classmethod
    def generate_django_orm_model(cls, reactant) -> DjangoModel:
        table_name = reactant.__name__
        columns = cls._get_columns(reactant)
        model = DjangoModel(name=table_name, fields=columns)
        return model

    @classmethod
    def _get_columns(cls, reactant) -> List[FieldOptions]:
        column_list = []
        for name, value in reactant.__fields__.items():
            column_type = cls._map_type_to_orm_field(value)
            extras = {}

            if not issubclass(type(value.field_info.default), UndefinedType):
                extras["default"] = value.field_info.default
            if value.field_info.extra:
                for k, v in value.field_info.extra.items():
                    extras[k] = v
            if value.required == False:
                extras["null"] = True
            if value.field_info.max_length:
                extras["max_length"] = value.field_info.max_length
            if value.field_info.title:
                extras["verbose_name"] = value.field_info.title
            if "foreign_key" in value.field_info.extra.keys():
                column_type.__name__ = "ForeignKey"
                extras["relation"] = value.field_info.extra["foreign_key"]
                extras["on_delete"] = "models.CASCADE"
                extras.pop("foreign_key")
            if "many_key" in value.field_info.extra.keys():
                column_type.__name__ = "ManyToManyField"
                extras["relation"] = value.field_info.extra["many_key"]
                extras.pop("many_key")
            if "one_key" in value.field_info.extra.keys():
                column_type.__name__ = "OneToOneField"
                extras["relation"] = value.field_info.extra["one_key"]
                extras["on_delete"] = "models.CASCADE"
                extras.pop("one_key")
            if (
                column_type.__name__ == "CharField"
                and value.field_info.max_length is None
            ):
                extras["max_length"] = 64

            column_info = FieldOptions(
                name=name, type=column_type.__name__, extras=extras
            )
            column_list.append(column_info)

        return column_list

    @classmethod
    def _map_type_to_orm_field(cls, field: ModelField) -> Any:
        if issubclass(field.type_, str):
            return CharField
        if issubclass(field.type_, float):
            return FloatField
        if issubclass(field.type_, bool):
            return BooleanField
        if issubclass(field.type_, int):
            return IntegerField
        if issubclass(field.type_, datetime):
            return DateTimeField
        if issubclass(field.type_, date):
            return DateField
        if issubclass(field.type_, timedelta):
            return DurationField
        if issubclass(field.type_, time):
            return TimeField
        if issubclass(field.type_, bytes):
            return BinaryField
        if issubclass(field.type_, Decimal):
            return DecimalField
        if issubclass(field.type_, ipaddress.IPv4Address):
            return GenericIPAddressField
        if issubclass(field.type_, ipaddress.IPv4Network):
            return GenericIPAddressField
        if issubclass(field.type_, ipaddress.IPv6Address):
            return GenericIPAddressField
        if issubclass(field.type_, ipaddress.IPv6Network):
            return GenericIPAddressField
        if issubclass(field.type_, Path):
            return CharField
        if issubclass(field.type_, uuid.UUID):
            return UUIDField
