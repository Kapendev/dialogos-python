import random
from dialogos import *


def actor(content: str) -> Line:
    return text("__actor", content)


def random_name(actor_name: str) -> str:
    name = actor_name
    while name == actor_name:
        name = random.choice(
            ("Liam", "Charlotte", "Oliver", "Amelia", "Elijah", "Noah")
        )
    return name


d = Dialogue([])
d.procedures["random_name"] = random_name
d.change(
    [
        variable("actor", "__random_name()"),
        actor("Hi!"),
        actor("I'm __actor and this is my friend __random_name(__actor)."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
