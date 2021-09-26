import ipaddress
import uuid

from typing import Any, Dict, NamedTuple, List, Sequence, Tuple, Type
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
    valid_arguments: List[str] = [
        # general
        "null",
        "blank",
        "choices",
        "db_column",
        "db_index",
        "db_tablespace",
        "default",
        "editable",
        "error_messages",
        "help_text",
        "primary_key",
        "unique",
        "unique_for_date",
        "unique_for_month",
        "unique_for_year",
        "verbose_name",
        "validators",
        # foreign key extras
        "foreign_key",
        "limit_choices_to",
        "related_name",
        "related_query_name",
        "to_field",
        "db_constraint",
        "swappable",
        # many-to-many extras
        "many_key",
        "symmetrical",
        "through",
        "through_fields",
        "db_table",
        "db_constraint",
        # one-to-one extras
        "one_key",
        "parent_link",
        # other extras
        "db_collation",
        "auto_now",
        "auto_now_add",
        "max_digits",
        "decimal_places",
        "protocol",
        "unpack_ipv4",
    ]

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
            column_type_final, extras_list = cls._filter_field_arguments(
                column_type, value
            )

            column_info = FieldOptions(
                name=name, type=column_type_final.__name__, extras=extras_list
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

    @classmethod
    def _filter_field_arguments(cls, column_type: Any, value: Any) -> Sequence[Any]:
        """
        This will filter out options that are not valid for the given Field type,
        and set defaults for required arguments that are not specified by the reactant model.
        """

        new_extra_options = {
            k: value.field_info.extra[k]
            for k in cls.valid_arguments
            if k in value.field_info.extra
        }

        extras_list = []

        if not issubclass(type(value.field_info.default), UndefinedType):
            extras_list.append({"default": value.field_info.default})
        if new_extra_options:
            for k, v in new_extra_options.items():
                if k == "foreign_key":
                    column_type.__name__ = "ForeignKey"
                    extras_list.insert(
                        0, {"relation": new_extra_options["foreign_key"]}
                    )
                    extras_list.insert(1, {"on_delete": "models.CASCADE"})
                elif k == "many_key":
                    column_type.__name__ = "ManyToManyField"
                    extras_list.insert(0, {"relation": new_extra_options["many_key"]})
                elif k == "one_key":
                    column_type.__name__ = "OneToOneField"
                    extras_list.insert(0, {"relation": new_extra_options["one_key"]})
                    extras_list.insert(1, {"on_delete": "models.CASCADE"})
                else:
                    extras_list.append({f"{k}": v})
        if value.required == False:
            extras_list.append({"null": True})
        if value.field_info.max_length:
            extras_list.append({"max_length": value.field_info.max_length})
        if value.field_info.title:
            extras_list.append({"verbose_name": value.field_info.title})
        if column_type.__name__ == "CharField" and value.field_info.max_length is None:
            extras_list.append({"max_length": 64})

        return (column_type, extras_list)
