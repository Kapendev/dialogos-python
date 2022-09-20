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


def do_things(_: str) -> str:
    print("  (I'm doing things...)  ")
    return ""


d = Dialogue()
d.procedures["random_name"] = random_name
d.procedures["do_things"] = do_things
d.change(
    [
        variable("actor", "!!random_name()"),
        variable("friend", "!!random_name(__actor)"),
        comment("!!do_things()"),
        actor("Hi!"),
        actor("I'm __actor and this is my friend __friend."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
