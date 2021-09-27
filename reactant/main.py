from pydantic import BaseModel
from click import secho
from typing import (
    Any,
    List,
    Tuple,
)


class Reactant(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


class DjangoORM(Reactant):
    def __str__(self):
        return "django"


class PeeweeORM(Reactant):
    def __str__(self):
        return "peewee"


class SQLAlchemyORM(Reactant):
    def __str__(self):
        return "sqlalchemy"


def classify_reactants() -> Tuple[List[Any], ...]:
    dj_classes = [cls for cls in DjangoORM.__subclasses__()]
    alchemy_classes = [cls for cls in SQLAlchemyORM.__subclasses__()]
    peewee_classes = [cls for cls in PeeweeORM.__subclasses__()]

    return (dj_classes, alchemy_classes, peewee_classes)


def generate() -> None:
    """
    Deliver Reactant models to appropriate CombustionChamber.
    CombustionChamber classes contain methods for rendering specific files
    according to the selected Reactant subclass.
    """

    dj_classes, alchemy_classes, peewee_classes = classify_reactants()

    if dj_classes:
        from reactant.renderer.django import DjangoCombustionChamber

        secho(f"Found {len(dj_classes)} Django reactants.", fg="blue")
        dj_rxn = DjangoCombustionChamber(dj_classes)
        dj_rxn.render_manager()
    else:
        secho("No Django reactants found.", fg="blue")

    if peewee_classes:
        from reactant.renderer.peewee import PeeweeCombustionChamber

        secho(f"Found {len(peewee_classes)} Peewee reactants.", fg="blue")
        pw_rxn = PeeweeCombustionChamber(peewee_classes)
        pw_rxn.render_manager()
    else:
        secho("No Peewee reactants found.", fg="blue")
