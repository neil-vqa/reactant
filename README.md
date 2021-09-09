# reactant

(WIP) Generate code for *models, views, and urls* based on Python type annotations. Powered by [pydantic](https://github.com/samuelcolvin/pydantic/). Influenced by [SQLModel](https://github.com/tiangolo/sqlmodel).

*reactant* aims to be non-intrusive and disposable as possible, but also to give usable and sensible code defaults.

Who wants an entire new dependency just to generate code? I don't, she doesn't, he doesn't, we don't! So, if you're like us, just spawn a new virtual environment somewhere for this. **CLI is coming soon** though.

## Roadmap

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
