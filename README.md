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

## 🐕 Example

A hello-world example.
More examples can be found in the examples folder.

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
python3 -m pip install git+https://github.com/AlexandrosKap/dialogos-python.git
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
