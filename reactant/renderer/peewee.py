from pathlib import Path
from typing import Any, Iterable, List, Tuple, Type

from black import FileMode, format_str
from click import secho
from jinja2 import Environment, PackageLoader

from reactant.exceptions import RenderFailed
from reactant.main import PeeweeORM
from reactant.orm.peewee import PeeweeCombustor, PeeweeModel

env = Environment(
    loader=PackageLoader("reactant"),
    trim_blocks=True,
)


class PeeweeCombustionChamber:
    """This class contains methods for rendering the files. Processes PeeweeORM subclasses."""

    def __init__(self, reactants: List[Type[PeeweeORM]]) -> None:
        self.reactants = reactants

    def get_models(self) -> List[PeeweeModel]:
        models = []
        for reactant in self.reactants:
            try:
                model = PeeweeCombustor.generate_peewee_orm_model(reactant)
                models.append(model)
            except Exception:
                raise
        return models

    def render_manager(self) -> None:
        try:
            models = self.get_models()
            fields_list = []
            for model in models:
                for field in model.fields:
                    fields_list.append(field.type)
            fields_set = set(fields_list)
            models_code, models_name_str = self.render_models(models, fields_set)
            self.write_to_file(models_code, models_name_str)
        except Exception:
            raise

    def render_models(
        self, models: List[PeeweeModel], fields_set: Iterable
    ) -> Tuple[str, str]:
        item_name = "models"
        try:
            template_models = env.get_template("peewee_models.txt.jinja")
            output_models = template_models.render(models=models, fields_set=fields_set)
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_models, item_name)

    def write_to_file(self, item: Any, item_name: str) -> None:
        try:
            p = Path("reactant_products/peewee")
            p.mkdir(parents=True, exist_ok=True)
            formatted_code = format_str(item, mode=FileMode())
            with open(f"{p}/{item_name}.py", "w") as file:
                file.write(formatted_code)
        except Exception:
            raise
        else:
            self._success_secho(item_name)

    def _success_secho(self, item_name: str):
        return secho(f"Peewee {item_name}.py finished rendering.", fg="green")
