import ipaddress
import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Sequence

from pydantic.fields import ModelField
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Interval,
    LargeBinary,
    Numeric,
    String,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID


class SQLAlchemyModelField(NamedTuple):
    name: str
    type: str
    extras: List[Dict[Any, Any]]


class SQLAlchemyModel(NamedTuple):
    name: str
    fields: List[SQLAlchemyModelField]


class SQLAlchemyCombustor:
    """
    This class contains methods for creating a SQLAlchemyModel tuple
    to be used by jinja templates to render the SQLAlchemy models.
    """

    @classmethod
    def generate_sqla_orm_models(cls, reactant) -> SQLAlchemyModel:
        table_name = reactant.__name__
        columns = cls._get_columns(reactant)
        model = SQLAlchemyModel(name=table_name, fields=columns)
        return model

    @classmethod
    def _get_columns(cls, reactant) -> List[SQLAlchemyModelField]:
        """Builds the list of fields for a model."""
        column_list = []
        for name, value in reactant.__fields__.items():
            column_type = cls._map_type_to_orm_field(value)
            column_type_final, extras_list = cls._filter_field_arguments(
                column_type, value
            )

            column_info = SQLAlchemyModelField(
                name=name, type=column_type_final.__name__, extras=extras_list
            )
            column_list.append(column_info)

        return column_list

    @classmethod
    def _map_type_to_orm_field(cls, field: ModelField) -> Any:
        if issubclass(field.type_, str):
            return String
        if issubclass(field.type_, float):
            return Float
        if issubclass(field.type_, bool):
            return Boolean
        if issubclass(field.type_, int):
            return Integer
        if issubclass(field.type_, datetime):
            return DateTime
        if issubclass(field.type_, date):
            return Date
        if issubclass(field.type_, timedelta):
            return Interval
        if issubclass(field.type_, time):
            return Time
        if issubclass(field.type_, Enum):
            return Enum
        if issubclass(field.type_, bytes):
            return LargeBinary
        if issubclass(field.type_, Decimal):
            return Numeric
        if issubclass(field.type_, ipaddress.IPv4Address):
            return String
        if issubclass(field.type_, ipaddress.IPv4Network):
            return String
        if issubclass(field.type_, ipaddress.IPv6Address):
            return String
        if issubclass(field.type_, ipaddress.IPv6Network):
            return String
        if issubclass(field.type_, Path):
            return String
        if issubclass(field.type_, uuid.UUID):
            return UUID

    @classmethod
    def _filter_field_arguments(cls, column_type: Any, value: Any) -> Sequence[Any]:
        """
        This will filter out arguments that are not valid for SQLAlchemy model fields,
        and sets defaults for required argumenta that are not explicitly set in the reactant model.
        """

        pass
