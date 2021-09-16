<p align="center">
    <a href="https://pypi.org/project/reactant">
        <img width="1200" src="https://raw.githubusercontent.com/neil-vqa/reactant/main/reactant-logo-banner.png">
    </a>
</p>

Generate code for *models, views, and urls* based on Python type annotations. Powered by [pydantic](https://github.com/samuelcolvin/pydantic/). Influenced by [SQLModel](https://github.com/tiangolo/sqlmodel).

*reactant* aims to give usable and sensible code defaults. It does **not enforce** a particular application structure. Instead, it follows the default/minimal/common structure of the supported frameworks, and it is up to the developer to make use of the generated code to fit it to their application. Contributions are warmly welcomed if you believe a particular structure is widely used and can benefit from code generation.

## Supported Frameworks

*reactant* currently generates code for the following:

**Django REST** (in Django's *default* project structure i.e. by *apps*)

- [X] models
- [X] views (class-based API views, filename=*views_class.py*)
- [ ] views (function-based API views, filename=*views_function.py*)
- [X] serializers
- [X] urls (from class-based API views, filename=*urls_class.py*)
- [ ] urls (from function-based API views, filename=*urls_function.py*)

**Flask**

- [ ] models (Flask-SQLAlchemy)

**SQLAlchemy**

- [ ] models in Declarative Mapping

**Peewee**

- [X] models

## Installation

```cli
$ pip install reactant
```

## Get Started

Create *reactant* models by inheriting from `Reactant` , and from another auxiliary class: `DjangoORM`, `SQLAlchemyORM`, `PeeweeORM`. The example below uses `DjangoORM`. Your choice of ORM will determine what code and files will be generated.

```python
# generate.py

from typing import Optional
from reactant import Reactant, DjangoORM, Field, generate


class RocketEngine(Reactant, DjangoORM):
    name: str = Field(max_length=32, title="engine_name")
    manufacturer: str = Field(max_length=64)
    power_cycle: Optional[str] = Field("gas-generator", blank=True, max_length=32)
    thrust_weight_ratio: Optional[int] = None


class LaunchVehicle(Reactant, DjangoORM):
    name: str = Field(max_length=32)
    country: str = Field(blank=True, max_length=32)
    status: str
    total_launches: Optional[int]
    engine: str = Field(foreign_key="RocketEngine")

# Don't forget this block.
if __name__ == "__main__":
    generate()

```

Don't forget `generate()`. Run the code. 

```cli
$ reactant generate.py

Running generate.py
Found 2 Django reactants.
Django models.py finished rendering.
Django views_class.py finished rendering.
Django serializers.py finished rendering.
Django urls_class.py finished rendering.
Success! Please check "reactant_products" directory.
```

**BOOM!** With just the above code, the models, views, serializers, and urls (the *products*, for Django atleast) are generated. See images of the code below.

## Sample Code Generated

### Django REST

<section>
    <div style="display:flex;">
        <div>
            <img src="https://raw.githubusercontent.com/neil-vqa/reactant/main/screenshots/dj_01.png" width="auto">
        </div>
        <div>
            <img src="https://raw.githubusercontent.com/neil-vqa/reactant/main/screenshots/dj_02.png" width="auto">
        </div>
    </div>
    <div style="display:flex; height:auto;">
        <div>
            <img src="https://raw.githubusercontent.com/neil-vqa/reactant/main/screenshots/dj_03.png" width="auto">
        </div>
        <div>
            <img src="https://raw.githubusercontent.com/neil-vqa/reactant/main/screenshots/dj_04.png" width="auto">
        </div>
    </div>
</section>

## Development

The project uses Poetry to package and manage dependencies.

```cli
(venv)$ poetry install
```

Run tests.
```cli
pytest
```

## License

MIT License. For more information and legal terms, see the LICENSE file.
