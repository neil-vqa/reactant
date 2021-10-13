from pathlib import Path
from typing import Any, Iterable, List, Tuple, Type

from black import FileMode, format_str
from click import secho
from jinja2 import Environment, PackageLoader

from reactant.exceptions import RenderFailed
from reactant.main import DjangoORM
from reactant.orm.django import DjangoCombustor, DjangoModel
from reactant.utils import convert_to_snake

env = Environment(
    loader=PackageLoader("reactant"),
    trim_blocks=True,
)


class DjangoCombustionChamber:
    """This class contains methods for rendering the files. Processes DjangoORM subclasses."""

    def __init__(self, reactants: List[Type[DjangoORM]]) -> None:
        self.reactants = reactants

    def get_models(self) -> List[DjangoModel]:
        models = []
        for reactant in self.reactants:
            try:
                model = DjangoCombustor.generate_django_orm_model(reactant)
                models.append(model)
            except Exception:
                raise
        return models

    def render_manager(
        self, class_based: bool = True, function_based: bool = True
    ) -> None:
        """Invokes render_* methods then pass the rendered template strings to writing the file."""
        try:
            models = self.get_models()
            model_names = [model.name for model in models]

            models_code, models_name_str = self.render_models(models)
            serializers_code, serializers_name_str = self.render_serializers(
                models, model_names
            )
            self.write_to_file(models_code, models_name_str)
            self.write_to_file(serializers_code, serializers_name_str)

            if class_based:
                views_code, views_name_str = self.render_views_class(model_names)
                urls_code, urls_name_str = self.render_urls_class(model_names)
                self.write_to_file(views_code, views_name_str)
                self.write_to_file(urls_code, urls_name_str)

            if function_based:
                views_func_code, views_func_name_str = self.render_views_func(
                    model_names
                )
                urls_func_code, urls_func_name_str = self.render_urls_func(model_names)
                self.write_to_file(views_func_code, views_func_name_str)
                self.write_to_file(urls_func_code, urls_func_name_str)

        except Exception:
            raise

    def render_models(self, models: List[DjangoModel]) -> Tuple[str, str]:
        item_name = "models"
        try:
            template_models = env.get_template("django_models.txt.jinja")
            output_models = template_models.render(models=models)
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_models, item_name)

    def render_views_class(self, model_names: List[str]) -> Tuple[str, str]:
        item_name = "views_class"
        try:
            template_views = env.get_template("django_views_class.txt.jinja")
            output_views = template_views.render(names=model_names)
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_views, item_name)

    def render_views_func(self, model_names: List[str]) -> Tuple[str, str]:
        item_name = "views_func"
        try:
            snaked_model_names = [convert_to_snake(name) for name in model_names]
            paired_names = dict(zip(model_names, snaked_model_names))
            template_views_func = env.get_template("django_views_func.txt.jinja")
            output_views_func = template_views_func.render(names=paired_names)
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_views_func, item_name)

    def render_serializers(
        self, models: List[DjangoModel], model_names: List[str]
    ) -> Tuple[str, str]:
        item_name = "serializers"
        try:
            template_serializers = env.get_template("django_serializers.txt.jinja")
            output_serializers = template_serializers.render(
                models=models, names=model_names
            )
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_serializers, item_name)

    def render_urls_class(self, model_names: List[str]) -> Tuple[str, str]:
        item_name = "urls_class"
        try:
            snaked_model_names = [convert_to_snake(name) for name in model_names]
            paired_names = dict(zip(model_names, snaked_model_names))
            template_urls = env.get_template("django_urls_class.txt.jinja")
            output_urls = template_urls.render(names=paired_names)
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_urls, item_name)

    def render_urls_func(self, model_names: List[str]) -> Tuple[str, str]:
        item_name = "urls_func"
        try:
            snaked_model_names = [convert_to_snake(name) for name in model_names]
            template_urls = env.get_template("django_urls_func.txt.jinja")
            output_urls_func = template_urls.render(names=snaked_model_names)
        except Exception:
            raise RenderFailed(item_name)
        else:
            return (output_urls_func, item_name)

    def write_to_file(self, item: Any, item_name: str) -> None:
        """Rendered template strings are formatted before writing."""
        try:
            p = Path("reactant_products/django")
            p.mkdir(parents=True, exist_ok=True)
            formatted_code = format_str(item, mode=FileMode())
            with open(f"{p}/{item_name}.py", "w") as file:
                file.write(formatted_code)
        except Exception:
            raise
        else:
            self._success_secho(item_name)

    def _success_secho(self, item_name: str):
        return secho(f"Django {item_name}.py finished rendering.", fg="green")
