from dialogos import *

d = Dialogue(
    [
        text("uwu", "My recomendation is..."),
        text("owo", "ubunchu!"),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
