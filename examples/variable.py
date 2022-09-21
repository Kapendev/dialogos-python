from dialogos import *


def mia(content: str) -> Line:
    return text("Mia", content)


d = Dialogue(
    [
        variable("i", "0"),
        mia("What's your name?"),
        variable("i", "$i + 1"),
        mia("Do you like cats?"),
        variable("i", "$i + 1"),
        mia("..."),
        mia("I asked $i questions."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
