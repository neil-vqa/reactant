from typing import Any, List, Tuple

from click import secho
from pydantic import BaseModel


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


def generate(class_based: bool = True, function_based: bool = True) -> None:
    """
    Deliver Reactant models to appropriate CombustionChamber.
    CombustionChamber classes contain methods for rendering specific files
    according to the selected Reactant subclass.
    """

    dj_classes, _, peewee_classes = classify_reactants()
    base_directory = "reactant_products"

    if dj_classes:
        try:
            from reactant.renderer.django import DjangoCombustionChamber

            secho(f"Found {len(dj_classes)} Django reactants.", fg="blue")
            dj_rxn = DjangoCombustionChamber(dj_classes)
            dj_rxn.render_manager(
                class_based=class_based, function_based=function_based
            )
        except Exception:
            secho(f"Sorry. Something went wrong rendering Django files.", fg="red")
            raise
        else:
            secho(
                f'Success! Please check "{base_directory}/django" directory.',
                fg="cyan",
            )
    else:
        secho("No Django reactants found.", fg="blue")

    if peewee_classes:
        try:
            from reactant.renderer.peewee import PeeweeCombustionChamber

            secho(f"Found {len(peewee_classes)} Peewee reactants.", fg="blue")
            pw_rxn = PeeweeCombustionChamber(peewee_classes)
            pw_rxn.render_manager()
        except Exception:
            secho(f"Sorry. Something went wrong rendering Peewee files.", fg="red")
            raise
        else:
            secho(
                f'Success! Please check "{base_directory}/peewee" directory.',
                fg="cyan",
            )
    else:
        secho("No Peewee reactants found.", fg="blue")
