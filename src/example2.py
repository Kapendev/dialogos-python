# End Example

from dialogos import *


def momo(content): return text("Momo", content)


d = Dialogue([
    momo("Hello world."),
    momo("Something something."),
    end(),
    momo("The end."),
])

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
