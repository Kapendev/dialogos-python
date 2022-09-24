from dialogos import *


def nerd(content: str) -> Line:
    return text("Nerd", content)


d = Dialogue(
    [
        # Create a label.
        label("START"),
        nerd("I'd just like to interject for a moment."),
        nerd("What you’re referring to as Linux, is in fact, GNU/Linux."),
        # Jump to the label 'END'.
        jump("END"),
        nerd("Or as I’ve recently taken to calling it, GNU plus Linux."),
        nerd("Linux is not an operating system unto itself."),
        nerd("but rather another free component of a fully functioning GNU system."),
        nerd("Many computer users run a modified version of the GNU system every day."),
        nerd("Without realizing it."),
        # Create a label.
        label("END"),
        nerd("All the so-called Linux distros are really distros of GNU/Linux."),
    ]
)

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
