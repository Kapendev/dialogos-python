from dialogos import *


def einstein(content: str) -> Line:
    return text("Einstein", content)


d = Dialogue(
    [
        variable("n", "1 + 2"),
        einstein("1 + 2 = $n"),
        einstein("And..."),
        variable("n", "$n * $n"),
        einstein("3 * 3 = $n"),
        # Skip a line if '$n = 9' is not true.
        check("$n = 9"),
        einstein("I'm very good at math!"),
        # Skip a line if '$n ! 9' is not true.
        check("$n ! 9"),
        einstein("I did something wrong?"),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
