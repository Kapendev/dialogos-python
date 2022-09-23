# 📝 Dialogos

A super simple dialogue system for Python.

It's nothing special, but that's the point! It's something that just works.
This library is ideal for games that are made for a game jam.
For more complex games I would recommend extending Dialogos or using something else.

## 📦 Installation

```sh
# Clone the repo.
git clone https://github.com/AlexandrosKap/dialogos-python

# Change your working directory.
cd dialogos-python

# Install the package globally.
python3 -m pip install .
```

## 🐈 Features

- Easy to use
- Labels
- Menus
- Variables
- Mathematical operations
- Conditional statements
- Procedures

## 🐕 Examples

A Hello World example

```python
from dialogos import *

def alex(content): return text("Alex", content)

d = Dialogue([
    alex("Hello world."),
    alex("Something something."),
    alex("The end."),
])

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
```

A Menu example

```python
from dialogos import *

def gigi(content: str) -> Line: return text("Gigi", content)

d = Dialogue([
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
])

while not d.has_end():
    while d.has_menu():
        print()
        for i, choice in enumerate(d.choices()):
            print("({}) => {}".format(i, choice))
        print("(Default choice is (0).)\n")
        d.choose(0)
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
```

## 🐍 Info

This is a port of the [original](https://github.com/AlexandrosKap/dialogos) version written in Rust.
