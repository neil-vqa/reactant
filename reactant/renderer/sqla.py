from pathlib import Path
from typing import Any, Iterable, List, Tuple, Type

from black import FileMode, format_str
from click import secho
from jinja2 import Environment, PackageLoader

from reactant.exceptions import RenderFailed
from reactant.main import SQLAlchemyORM

env = Environment(
    loader=PackageLoader("reactant"),
    trim_blocks=True,
)


class SQLAlchemyCombustionChamber:
    """This class contains methods for rendering the files. Processes SQLAlchemyORM subclasses."""

    def __init__(self, reactants: List[Type[SQLAlchemyORM]]) -> None:
        self.reactants = reactants

    def get_models(self) -> List[Any]:
        pass
