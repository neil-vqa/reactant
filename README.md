# reactant

Generate code for *models, views, and urls* based on Python type annotations. Powered by [pydantic](https://github.com/samuelcolvin/pydantic/). Influenced by [SQLModel](https://github.com/tiangolo/sqlmodel).

*reactant* aims to be non-intrusive and disposable as possible, but also to give usable and sensible code defaults.

## Roadmap

**Django REST** (in Django's *default* project structure i.e. by *apps*)

- [X] models
- [X] views (class-based API views, filename=views_class.py)
- [ ] views (function-based API views, filename=views_function.py)
- [X] serializers
- [ ] urls

**SQLAlchemy**

- [ ] models in Declarative Mapping

**Peewee**

- [ ] models
