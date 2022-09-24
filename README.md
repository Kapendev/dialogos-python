# 📝 Dialogos

A super simple dialogue system for Python.

It's nothing special, but that's the point! It's something that just works.
This library is ideal for games that are made for a game jam.
For more complex games it is recommended to extend Dialogos or use something else.

## 🐈 Features

- Easy to use
- Labels
- Menus
- Variables
- Procedures
- Conditional statements
- Mathematical operations
- Syntax inspired by Assembly

## 🐕 Hello World Example

```python
from dialogos import *

d = Dialogue([
    # A line has info and content.
    text("uwu", "My recomendation is..."),
    text("owo", "ubunchu!"),
])

while not d.has_end():
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
```

## 📦 Installation

```sh
# Clone the repository.
git clone https://github.com/AlexandrosKap/dialogos-python

# Install the package globally.
python3 -m pip install dialogos-python
```

## 🐍 Info

This is a port of the [original](https://github.com/AlexandrosKap/dialogos) version written in Rust.
