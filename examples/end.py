from dialogos import *


def momo(content: str) -> Line:
    return text("Momo", content)


d = Dialogue(
    [
        momo("Hi!"),
        # End the dialogue.
        end(),
        momo("Can you see me?"),
        momo("No?"),
        momo("..."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
