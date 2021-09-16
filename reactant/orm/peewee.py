import ipaddress
import uuid

from typing import Any, Dict, NamedTuple, List, Type
from pydantic.fields import ModelField, UndefinedType

from datetime import date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from peewee import (
    CharField,
    FloatField,
    BooleanField,
    IntegerField,
    DateTimeField,
    DateField,
    TimeField,
    BlobField,
    DecimalField,
    IPField,
    UUIDField,
)


class PeeweeORM:
    def __str__(self):
        return "peewee"


class FieldOptions(NamedTuple):
    name: str
    type: str
    extras: List[Dict[Any, Any]]


class PeeweeModel(NamedTuple):
    name: str
    fields: List[FieldOptions]


class PeeweeCombustor:
    @classmethod
    def generate_peewee_orm_model(cls, reactant) -> PeeweeModel:
        table_name = reactant.__name__
        columns = cls._get_columns(reactant)
        model = PeeweeModel(name=table_name, fields=columns)
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
                        extras_list.insert(0, {"relation": v})
                    else:
                        extras_list.append({f"{k}": v})
            if value.required == False:
                extras_list.append({"null": True})
            if value.field_info.max_length:
                extras_list.append({"max_length": value.field_info.max_length})
            if value.field_info.title:
                extras_list.append({"verbose_name": value.field_info.title})
            if "foreign_key" in value.field_info.extra.keys():
                column_type.__name__ = "ForeignKeyField"
            if (
                column_type.__name__ == "CharField"
                and value.field_info.max_length is None
            ):
                extras_list.append({"max_length": 255})

            column_info = FieldOptions(
                name=name, type=column_type.__name__, extras=extras_list
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
        if issubclass(field.type_, time):
            return TimeField
        if issubclass(field.type_, bytes):
            return BlobField
        if issubclass(field.type_, Decimal):
            return DecimalField
        if issubclass(field.type_, ipaddress.IPv4Address):
            return IPField
        if issubclass(field.type_, ipaddress.IPv4Network):
            return IPField
        if issubclass(field.type_, Path):
            return CharField
        if issubclass(field.type_, uuid.UUID):
            return UUIDField
