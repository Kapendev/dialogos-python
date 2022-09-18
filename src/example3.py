# Label Example

from dialogos import *


def ferris(content): return text("Ferris", content)


d = Dialogue([
    label("The Beginning"),
    ferris("Hello world."),
    jump("The End"),
    ferris("Something something."),
    ferris("The end."),
    label("The End")
])

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
