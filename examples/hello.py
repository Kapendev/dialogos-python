from dialogos import *

d = Dialogue(
    [
        # A line has info and content.
        text("uwu", "My recomendation is..."),
        text("owo", "ubunchu!"),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
