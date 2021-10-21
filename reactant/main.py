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


def generate_django(dj_classes, base_directory, class_based, function_based) -> None:
    try:
        from reactant.renderer.django import DjangoCombustionChamber

        # DjangoCombustionChamber class contains methods for generating the files.
        secho(f"Found {len(dj_classes)} Django reactants.", fg="blue")
        dj_rxn = DjangoCombustionChamber(dj_classes)
        dj_rxn.render_manager(class_based=class_based, function_based=function_based)
    except ImportError:
        secho(
            "Failed to import django. Please install django to generate django files.",
            fg="red",
        )
    except Exception:
        secho(f"Sorry. Something went wrong rendering Django files.", fg="red")
        raise
    else:
        secho(
            f'Success! Please check "{base_directory}/django" directory.',
            fg="cyan",
        )


def generate_peewee(peewee_classes, base_directory) -> None:
    try:
        from reactant.renderer.peewee import PeeweeCombustionChamber

        # PeeweeCombustionChamber class contains methods for generating the files.
        secho(f"Found {len(peewee_classes)} Peewee reactants.", fg="blue")
        pw_rxn = PeeweeCombustionChamber(peewee_classes)
        pw_rxn.render_manager()
    except ImportError:
        secho(
            "Failed to import peewee. Please install peewee to generate peewee files.",
            fg="red",
        )
    except Exception:
        secho(f"Sorry. Something went wrong rendering Peewee files.", fg="red")
        raise
    else:
        secho(
            f'Success! Please check "{base_directory}/peewee" directory.',
            fg="cyan",
        )


def generate_sqla(alchemy_classes, base_directory) -> None:
    try:
        from reactant.renderer.sqla import SQLAlchemyCombustionChamber

        # SQLAlchemyCombustionChamber class contains methods for generating the files.
        secho(f"Found {len(alchemy_classes)} SQLAlchemy reactants.", fg="blue")
        pw_rxn = SQLAlchemyCombustionChamber(alchemy_classes)
        pw_rxn.render_manager()
    except ImportError:
        secho(
            "Failed to import sqlalchemy. Please install sqlalchemy to generate the files.",
            fg="red",
        )
    except Exception:
        secho(f"Sorry. Something went wrong rendering SQLAlchemy files.", fg="red")
        raise
    else:
        secho(
            f'Success! Please check "{base_directory}/sqla" directory.',
            fg="cyan",
        )


def generate(class_based: bool = True, function_based: bool = True) -> None:
    """
    Deliver Reactant models to appropriate "generators".
    """

    dj_classes, alchemy_classes, peewee_classes = classify_reactants()
    base_directory = "reactant_products"

    if dj_classes:
        generate_django(dj_classes, base_directory, class_based, function_based)
    else:
        secho("No Django reactants found.", fg="blue")

    if peewee_classes:
        generate_peewee(peewee_classes, base_directory)
    else:
        secho("No Peewee reactants found.", fg="blue")

    if alchemy_classes:
        generate_sqla(alchemy_classes, base_directory)
    else:
        secho("No SQLAlchemy reactants found.", fg="blue")
