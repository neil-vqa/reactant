import ipaddress
import uuid
from reactant.main import DjangoORM, Reactant
from pydantic.fields import ModelField
from datetime import date, datetime, time, timedelta
from enum import Enum
from decimal import Decimal
from pathlib import Path
from typing import NamedTuple, List
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


def generate_django_orm_models(dj_subclass: DjangoORM) -> NamedTuple:
    columns = get_columns(dj_subclass)
    model_name = dj_subclass.__name__
    DjangoModel = NamedTuple("DjangoModel", [("name", str), ("fields", List)])
    model = DjangoModel(name=model_name, fields=columns)
    return model


def get_columns(dj_subclass: Reactant) -> List:
    column_list = []
    for key, value in dj_subclass.__fields__.items():
        column_type = map_type_to_orm_field(value)
        column_info = {"name": key, "column_type": column_type.__name__}
        column_list.append(column_info)
    return column_list


def map_type_to_orm_field(field: ModelField):
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
