from dialogos import *


def einstein(content: str) -> Line:
    return text("Einstein", content)


d = Dialogue(
    [
        variable("val", "1 + 2"),
        einstein("1 + 2 = $val"),
        einstein("And..."),
        variable("val", "$val * $val"),
        einstein("3 * 3 = $val"),
        # Check if the math is bad.
        check("$val == 9"),
        einstein("I'm very good at math!"),
        check("$val != 9"),
        einstein("I did something wrong?"),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
