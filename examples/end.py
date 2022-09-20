from dialogos import *


def momo(content: str) -> Line:
    return text("Momo", content)


d = Dialogue(
    [
        momo("Hello world."),
        end(),
        momo("Something something."),
        momo("The end."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
