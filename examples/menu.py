from dialogos import *


def gigi(content: str) -> Line:
    return text("Gigi", content)


d = Dialogue(
    [
        gigi("What should I do?"),
        # Jump to the label 'COFFE', 'TEA' or 'SLEEP'.
        menu("COFFEE||TEA||SLEEP", "Drink coffee.||Drink tea.||Go sleep."),
        label("COFFEE"),
        gigi("I drink the coffee."),
        end(),
        label("TEA"),
        gigi("I drink the tea."),
        end(),
        label("SLEEP"),
        gigi("I drink the sleep."),
    ]
)

while not d.has_end():
    while d.has_menu():
        print()
        for i, choice in enumerate(d.choices()):
            print("{}| {}".format(i + 1, choice))
        print("Default choice: (1)\n")
        d.choose(0)
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
