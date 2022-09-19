# Label Example

from dialogos import *


def ferris(content: str) -> Line:
    return text("Ferris", content)


d = Dialogue(
    [
        label("START"),
        ferris("Hello world."),
        jump("END"),
        ferris("Something something."),
        label("END"),
        ferris("The end."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
