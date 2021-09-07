from reactant import Reactant, create_all


class Airplane(Reactant):
    id: int
    name: str
    airline: str


class Ship(Reactant):
    id: int
    name: str
    company: str


# user1 = User(id=123, username="jihyo")

# print(type(user1))
# print(user1.__annotations__)
# print(user1.__dict__)
# print(user1.annotations())


if __name__ == "__main__":
    create_all()
