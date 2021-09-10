import ipaddress
import uuid
from pydantic.fields import ModelField, UndefinedType
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, NamedTuple, List
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
    extras: Dict[Any, Any]


class DjangoModel(NamedTuple):
    name: str
    fields: List[FieldOptions]


class DjangoORM:
    def generate_django_orm_models(self) -> DjangoModel:
        model_name = self.__name__
        columns = self._get_columns(self)
        model = DjangoModel(name=model_name, fields=columns)
        return model

    def _get_columns(self) -> List[FieldOptions]:
        column_list = []
        for name, value in self.__fields__.items():
            column_type = self._map_type_to_orm_field(value)
            extras = {}

            if not issubclass(type(value.field_info.default), UndefinedType):
                extras["default"] = value.field_info.default
            if value.field_info.extra:
                for k, v in value.field_info.extra.items():
                    extras[k] = v
            if value.field_info.max_length:
                extras["max_length"] = value.field_info.max_length
            if value.field_info.title:
                extras["verbose_name"] = value.field_info.title

            column_info = FieldOptions(
                name=name, type=column_type.__name__, extras=extras
            )
            column_list.append(column_info)

        return column_list

    def _map_type_to_orm_field(field: ModelField) -> Any:
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
