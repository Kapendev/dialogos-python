# 📝 Dialogos

A super simple dialogue system for Python.

It's nothing special, but that's the point! It's something that just works.
This library is ideal for games that are made for a game jam.
For more complex games I would recommend extending Dialogos or using something else.

## 🐈 Features

- Easy to use
- Labels
- Menus
- Variables
- Mathematical operations
- Conditional statements

## 🐕 Example

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

## 🐍 Info

This is a port of the [original](https://github.com/AlexandrosKap/dialogos) version written in Rust.
