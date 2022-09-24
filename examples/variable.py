from dialogos import *


def mia(content: str) -> Line:
    return text("Mia", content)


d = Dialogue(
    [
        # Create variable.
        variable("count", "0"),
        mia("What's your name?"),
        # Change variable.
        variable("count", "$count + 1"),
        mia("Do you like cats?"),
        variable("count", "$count + 1"),
        mia("..."),
        # Use variable with the '$' character.
        mia("I asked $count questions."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
