import random
from dialogos import *


def actor(content: str) -> Line:
    return text("$actor", content)


def random_name(actor_name: str) -> str:
    name = actor_name
    while name == actor_name:
        name = random.choice(
            ("Liam", "Charlotte", "Oliver", "Amelia", "Elijah", "Noah")
        )
    return name


def foo(s: str) -> str:
    n = int(s)
    print("  ({})(I'm doing things...)  ".format(n))
    n -= 1
    return str(n)


d = Dialogue()
d.procedures["random_name"] = random_name
d.procedures["foo"] = foo
d.change(
    [
        variable("actor", "$$random_name()"),
        variable("friend", "$$random_name($actor)"),
        comment("$$foo(1)"),
        actor("Hi!"),
        actor("I'm $actor and this is my friend $friend."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
