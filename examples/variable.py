# Variable Example

from dialogos import *


def mia(content: str) -> Line:
    return text("Mia", content)


def alucard(content: str) -> Line:
    return text("__name", content)


d = Dialogue(
    [
        variable("name", "???"),
        mia("What's your name?"),
        alucard("They call me Alucard."),
        variable("name", "Alucard"),
        mia("__name..."),
        mia("HAHAHA!"),
        alucard("What?"),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
