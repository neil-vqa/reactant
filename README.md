<p align="center">
    <a href="#">
        <img width="1200" src="https://raw.githubusercontent.com/neil-vqa/reactant/main/reactant-logo.png">
    </a>
</p>

(WIP) Generate code for *models, views, and urls* based on Python type annotations. Powered by [pydantic](https://github.com/samuelcolvin/pydantic/). Influenced by [SQLModel](https://github.com/tiangolo/sqlmodel).

*reactant* aims to be non-intrusive and disposable as possible, but also to give usable and sensible code defaults.

Who wants an entire new dependency just to generate code? I don't, she doesn't, he doesn't, we don't! So, if you're like us, just spawn a new virtual environment somewhere for this.

## Supported Frameworks

*reactant* currently generates code for the following:

**Django REST** (in Django's *default* project structure i.e. by *apps*)

- [X] models
- [X] views (class-based API views, filename=*views_class.py*)
- [ ] views (function-based API views, filename=*views_function.py*)
- [X] serializers
- [X] urls (from class-based API views, filename=*urls_class.py*)
- [ ] urls (from function-based API views, filename=*urls_function.py*)

**SQLAlchemy**

- [ ] models in Declarative Mapping

**Peewee**

- [ ] models

## Installation

Coming soon to PyPI.

## Get Started

Create *reactant* models by inheriting from `Reactant` , and from choosing an ORM: `DjangoORM`, `SQLAlchemyORM`, `PeeweeORM`. The example below uses `DjangoORM`. Your choice of ORM will determine what code and files will be generated.

```python

from typing import Optional
from reactant import Reactant, DjangoORM, generate, Field


class RocketEngine(Reactant, DjangoORM):
    id: int = Field(primary_key=True, title="rocket_id")
    name: str = Field(max_length=32)
    manufacturer: str = Field(max_length=64)
    power_cycle: Optional[str] = Field(
        "gas-generator", nullable=True, blank=True, max_length=32
    )
    thrust_weight_ratio: int


class LaunchVehicle(Reactant, DjangoORM):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=32)
    country: str = Field(blank=True, max_length=32)


if __name__ == "__main__":
    generate()

```

Don't forget `generate()`. Run the code. **BOOM!** With the above code, the models, views, serializers, and urls (for Django atleast) are generated, the *by-product of your reactants*.