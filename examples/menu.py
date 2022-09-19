# Menu Example

from dialogos import *


def gigi(content: str) -> Line:
    return text("Gigi", content)


d = Dialogue(
    [
        gigi("What should I do?"),
        menu("Coffee||Tea||Sleep", "Drink coffee.||Drink tea.||Go sleep."),
        label("Coffee"),
        gigi("I drink the coffee."),
        end(),
        label("Tea"),
        gigi("I drink the tea."),
        end(),
        label("Sleep"),
        gigi("I drink the sleep."),
    ]
)

while not d.has_end():
    while d.has_menu():
        print()
        for i, choice in enumerate(d.choices()):
            print("{} => {}".format(i + 1, choice))
        print("(Default choice is 1.)\n")
        d.choose(0)
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
