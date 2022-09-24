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

# Run an example.
cd examples
python3 hello.py
```

## 🐈 Features

- Easy to use
- Labels
- Menus
- Variables
- Mathematical operations
- Conditional statements
- Procedures

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

## 🐍 Info

This is a port of the [original](https://github.com/AlexandrosKap/dialogos) version written in Rust.
