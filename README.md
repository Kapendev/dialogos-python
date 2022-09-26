# 📝 Dialogos

A super simple dialogue system for Python.

The library provides the essential tools needed to create a dialogue for a game, allowing you to focus on the specific needs of your project.
It is simple by default, but can easily be extended to something powerful when needed.

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

## 📖 Documentation

The API documentation can be found in the docs folder.
You can read it by opening the index.html file with your web browser.

## 📦 Installation

Copy and paste the following commands into your terminal.
Windows users may have to write python instead of python3.

```sh
python3 -m pip install git+https://github.com/AlexandrosKap/dialogos-python.git
```

## 📜 License

The project is released under the terms of the MIT License.
Please refer to the LICENSE file.
