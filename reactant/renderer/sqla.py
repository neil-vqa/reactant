from pathlib import Path
from typing import Any, Iterable, List, Tuple, Type

from black import FileMode, format_str
from click import secho
from jinja2 import Environment, PackageLoader

from reactant.exceptions import RenderFailed
from reactant.main import SQLAlchemyORM
from reactant.orm.sqla import SQLAlchemyCombustor, SQLAlchemyModel
from reactant.utils import convert_to_snake

env = Environment(
    loader=PackageLoader("reactant"),
    trim_blocks=True,
)


class SQLAlchemyCombustionChamber:
    """This class contains methods for rendering the files. Processes SQLAlchemyORM subclasses."""

    def __init__(self, reactants: List[Type[SQLAlchemyORM]]) -> None:
        self.reactants = reactants

    def get_models(self) -> List[SQLAlchemyModel]:
        models = []
        for reactant in self.reactants:
            try:
                model = SQLAlchemyCombustor.generate_sqla_orm_models(reactant)
                models.append(model)
            except Exception:
                raise
        return models

    def render_manager(self) -> None:
        models = self.get_models()
        fields_list = []
        for model in models:
            for field in model.fields:
                fields_list.append(field.type)
        fields_set = set(fields_list)

        dec_models_code, dec_name_str = self.render_declarative_models(
            models, fields_set
        )
        clas_models_code, clas_name_str = self.render_classical_models(
            models, fields_set
        )

        self.write_to_file(dec_models_code, dec_name_str)
        self.write_to_file(clas_models_code, clas_name_str)

    def render_declarative_models(
        self, models: List[SQLAlchemyModel], fields_set: Iterable
    ) -> Tuple[str, str]:
        item_name = "declarative_models"
        try:
            template_mod = env.get_template("sqla_models_declarative.txt.jinja")
            output_dec_models = template_mod.render(
                models=models, convert_to_snake=convert_to_snake, fields_set=fields_set
            )
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_dec_models, item_name)

    def render_classical_models(
        self, models: List[SQLAlchemyModel], fields_set: Iterable
    ) -> Tuple[str, str]:
        item_name = "classical_models"
        try:
            template_mod = env.get_template("sqla_models_classical.txt.jinja")
            output_clas_models = template_mod.render(
                models=models, convert_to_snake=convert_to_snake, fields_set=fields_set
            )
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_clas_models, item_name)

    def write_to_file(self, item: Any, item_name: str) -> None:
        try:
            p = Path("reactant_products/sqla")
            p.mkdir(parents=True, exist_ok=True)
            formatted_code = format_str(item, mode=FileMode())
            with open(f"{p}/{item_name}.py", "w") as file:
                file.write(formatted_code)
        except Exception:
            raise
        else:
            self._success_secho(item_name)

    def _success_secho(self, item_name: str):
        return secho(f"SQLAlchemy {item_name}.py finished rendering.", fg="green")
