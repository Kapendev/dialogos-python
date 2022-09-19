# Check Example

from dialogos import *


def einstein(content: str) -> Line:
    return text("Einstein", content)


d = Dialogue(
    [
        variable("val", "1 + 2"),
        einstein("1 + 2 = __val"),
        einstein("And..."),
        variable("val", "__val * __val"),
        einstein("3 * 3 = __val"),
        # Check if the math is bad.
        check("__val == 9"),
        einstein("I'm very good at math!"),
        check("__val != 9"),
        einstein("I did something wrong?"),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
