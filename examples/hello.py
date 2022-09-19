# Hello Example

from dialogos import *


def alex(content: str) -> Line:
    return text("Alex", content)


d = Dialogue(
    [
        alex("Hello world."),
        alex("Something something."),
        alex("The end."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
