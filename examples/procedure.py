import random
from dialogos import *


def actor(content: str) -> Line:
    return text("$actor", content)


def random_name(reserved_name: str) -> str:
    name = reserved_name
    while name == reserved_name:
        name = random.choice(
            ("Liam", "Charlotte", "Oliver", "Amelia", "Elijah", "Noah")
        )
    return name


def foo(_: str) -> str:
    print("  (I'm doing things...)  ")
    return ""


d = Dialogue(
    [
        # Use procedures.
        variable("actor", "$random_name()"),
        variable("friend", "$random_name($actor)"),
        actor("$foo()Hi!"),
        actor("I'm $actor and this is my friend $friend."),
    ]
).add_procedures(
    {
        # Create procedures.
        "random_name": random_name,
        "foo": foo,
    }
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
