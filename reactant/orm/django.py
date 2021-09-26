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


class FieldOptions(NamedTuple):
    name: str
    type: str
    extras: List[Dict[Any, Any]]


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
            extras_list = []

            if not issubclass(type(value.field_info.default), UndefinedType):
                extras_list.append({"default": value.field_info.default})
            if value.field_info.extra:
                for k, v in value.field_info.extra.items():
                    if k == "foreign_key":
                        column_type.__name__ = "ForeignKey"
                        extras_list.insert(
                            0, {"relation": value.field_info.extra["foreign_key"]}
                        )
                        extras_list.append({"on_delete": "models.CASCADE"})
                    elif k == "many_key":
                        column_type.__name__ = "ManyToManyField"
                        extras_list.insert(
                            0, {"relation": value.field_info.extra["many_key"]}
                        )
                    elif k == "one_key":
                        column_type.__name__ = "OneToOneField"
                        extras_list.insert(
                            0, {"relation": value.field_info.extra["one_key"]}
                        )
                        extras_list.append({"on_delete": "models.CASCADE"})
                    else:
                        extras_list.append({f"{k}": v})
            if value.required == False:
                extras_list.append({"null": True})
            if value.field_info.max_length:
                extras_list.append({"max_length": value.field_info.max_length})
            if value.field_info.title:
                extras_list.append({"verbose_name": value.field_info.title})
            if (
                column_type.__name__ == "CharField"
                and value.field_info.max_length is None
            ):
                extras_list.append({"max_length": 64})

            column_info = FieldOptions(
                name=name, type=column_type.__name__, extras=extras_list
            )
            column_list.append(column_info)

        return column_list

    @classmethod
    def _map_type_to_orm_field(cls, field: ModelField) -> Any:
        """SQLModel-inspired."""

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
