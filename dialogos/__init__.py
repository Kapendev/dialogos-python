"""
.. include:: ../README.md
"""

import re
from typing import Optional, List, Dict, Callable

END_LINE = 0
TEXT_LINE = 1
LABEL_LINE = 2
JUMP_LINE = 3
MENU_LINE = 4
VARIABLE_LINE = 5
CHECK_LINE = 6
COMMENT_LINE = 7

SPLIT_PATTERN = "||"
VARIABLE_PATTERN = r"\$(\w+)"
PROCEDURE_PATTERN = r"\$(\w+)\((.*)\)"


class Line:
    """The dialogue line structure."""

    def __init__(self, t: int, info: str, content: str) -> None:
        """
        Creates a new line.

        Each line has a type and some information that defines how its content will be used by a system.
        """
        self.t = t
        """The line type."""
        self.info = info
        """The line info."""
        self.content = content
        """The content of the line."""

    def __repr__(self) -> str:
        return "Line(t: {}, info: '{}', content: '{}')".format(
            self.t, self.info, self.content
        )


class Dialogue:
    """The dialogue structure."""

    def __init__(self, lines: Optional[List[Line]] = None) -> None:
        """
        Creates a new dialogue.

        Every dialogue has variables and procedures.
        Variables store data and can be created inside and outside the dialogue.
        Procedures on the other hand, perform a task and can only be created outside the dialogue.
        """
        self.__index = 0
        self.__lines: List[Line] = []
        self.__labels: Dict[str, int] = {}
        self.__variables: Dict[str, str] = {}
        self.__procedures: Dict[str, Callable[[str], str]] = {}
        if lines is not None:
            self.change_lines(lines)

    def __repr__(self) -> str:
        return "Dialogue(index: {}, lines: {}, labels: {}, variables: {})".format(
            self.__index, self.__lines, self.__labels, self.__variables
        )

    def add_variables(self, new: Dict[str, str]) -> "Dialogue":
        """Adds new variables to the dialogue."""
        self.__variables.update(new)
        return self

    def add_procedures(self, new: Dict[str, Callable[[str], str]]) -> "Dialogue":
        """Adds new procedures to the dialogue."""
        self.__procedures.update(new)
        self.reset()
        return self

    def remove_variables(self, keys: List[str]) -> "Dialogue":
        """Removes variables from the dialogue."""
        for key in keys:
            del self.__variables[key]
        return self

    def remove_procedures(self, keys: List[str]) -> "Dialogue":
        """Removes procedures from the dialogue."""
        for key in keys:
            del self.__procedures[key]
        return self

    def change_variables(self, new: Dict[str, str]) -> "Dialogue":
        """Changes the variables of the dialogue."""
        self.__variables = new
        return self

    def change_procedures(self, new: Dict[str, Callable[[str], str]]) -> "Dialogue":
        """Changes the procedures of the dialogue."""
        self.__procedures = new
        return self

    def change_lines(self, new: List[Line]) -> "Dialogue":
        """Changes the lines of the dialogue."""
        self.__labels.clear()
        self.__lines = new
        for i, line in enumerate(self.__lines):
            if line.t == LABEL_LINE:
                self.__labels[line.content] = i
        self.__lines.append(end())
        self.reset()
        return self

    def __replace(self, s: str) -> str:
        """Replace parts of a string with values from variables and procedures."""
        result = s
        for match in re.finditer(VARIABLE_PATTERN, s):
            target = match.group()
            key = match.group(1)
            if key in self.__variables:
                result = result.replace(target, self.__variables[key])
        s = result
        for match in re.finditer(PROCEDURE_PATTERN, s):
            target = match.group()
            key = match.group(1)
            arg = match.group(2)
            if key in self.__procedures:
                result = result.replace(target, self.__procedures[key](arg))
        return result

    def line(self) -> Line:
        """Returns the current line of the dialogue."""
        line = self.__lines[self.__index]
        return Line(line.t, self.__replace(line.info), self.__replace(line.content))

    def goto(self, index: int) -> None:
        "Goes to a specific line of the dialogue."
        if index < 0:
            self.__index = 0
        elif index < len(self.__lines):
            self.__index = index
        else:
            self.__index = len(self.__lines) - 1
        self.__update()

    def next(self) -> None:
        """Goes to the next line of the dialogue."""
        self.goto(self.__index + 1)

    def jump(self, label: str) -> None:
        """Goes to a line of the dialogue by using a label."""
        self.goto(self.__labels[label])

    def reset(self) -> None:
        """Resets the dialogue index."""
        self.goto(0)

    def has_end(self) -> bool:
        """Returns true if the current line of the dialogue is an end line."""
        return self.__lines[self.__index].t == END_LINE

    def has_menu(self) -> bool:
        """Returns true if the current line of the dialogue is a menu line."""
        return self.__lines[self.__index].t == MENU_LINE

    def choices(self) -> List[str]:
        """Returns the choices of a menu line if the current line of the dialogue is a menu line."""
        line = self.__lines[self.__index]
        if line.t == MENU_LINE:
            return split(self.__replace(line.content))
        return []

    def choose(self, choice: int) -> None:
        """Chooses a label from the current menu line and jumps to it."""
        info = self.__lines[self.__index].info
        self.jump(split(self.__replace(info))[choice])

    def __update(self) -> None:
        """Updates the dialogue state."""
        # Calling update should not call procedures
        # when a text or menu line is processed.
        line = self.__lines[self.__index]
        if line.t != TEXT_LINE and line.t != MENU_LINE:
            line = self.line()
        # Do something for some types.
        if line.t == LABEL_LINE or line.t == COMMENT_LINE:
            self.next()
        elif line.t == JUMP_LINE:
            if line.content in self.__labels:
                self.jump(line.content)
            else:
                self.next()
        elif line.t == VARIABLE_LINE:
            value = calc(line.content)
            if value is not None:
                self.__variables[line.info] = str(
                    int(value) if value.is_integer() else value
                )
            else:
                self.__variables[line.info] = line.content
            self.next()
        elif line.t == CHECK_LINE:
            value = calc(line.content)
            if value is None:
                # Do string comparison if calc failed.
                args = line.content.split("=")
                if len(args) == 2 and args[0].strip() == args[1].strip():
                    self.next()
                else:
                    self.goto(self.__index + 2)
            elif value != 0.0:
                self.next()
            else:
                self.goto(self.__index + 2)


# Functions for processing strings.


def __expr(a: float, op: str, b: float) -> Optional[float]:
    """
    The calculation part of the calc function.

    Synthels quotes:
    - 🤓 'Bruh dude just use a dictionary with lambdas!'
    - 😎 'Bro you can use a tokenizer module...'
    - 😂 'Your implementation simply calculates each thing in a list in order.'
    """
    if op == "*":
        return a * b
    elif op == "/":
        return a / b
    elif op == ":":
        return a // b
    elif op == "%":
        return a % b
    elif op == "<":
        return float(a < b)
    elif op == ">":
        return float(a > b)
    elif op == "=":
        return float(a == b)
    elif op == "!":
        return float(a != b)
    else:
        return None


def calc(s: str) -> Optional[float]:
    """
    Parses and evaluates simple math expressions.

    Supported operators: +, -, *, /, :, %, <, >, =, !
    """
    args = s.replace(" ", "") + "+0"
    try:
        stack: List[float] = [0]
        r_op = "+"
        buffer = ""
        i = 0
        while i < len(args):
            if args[i] in "0123456789":
                buffer += args[i]
            else:
                l_op = r_op
                r_op = args[i]
                n = float(buffer) if buffer else None

                # Calculate expression inside parentheses.
                if n is None:
                    if r_op == "(" and i + 1 < len(args):
                        # Find the position of ')'.
                        count = 0
                        j = i + 1
                        while j < len(args):
                            if args[j] == "(":
                                count += 1
                            elif args[j] == ")":
                                if count == 0:
                                    break
                                count -= 1
                            j += 1
                        # Skip the characters in parentheses.
                        n = calc(args[i + 1 : j])
                        i = j + 1
                        if n is None or i >= len(args):
                            return None
                        r_op = args[i]
                    else:
                        return None

                # Calculate expression.
                if l_op == "+":
                    stack.append(n)
                elif l_op == "-":
                    stack.append(-n)
                else:
                    value = __expr(stack[-1], l_op, n)
                    if value is None:
                        return None
                    stack[-1] = value
                buffer = ""
            i += 1
        return sum(stack)
    except ValueError:
        return None


def split(s: str) -> List[str]:
    """Splits a string with the dialogue split pattern."""
    return s.strip().split(SPLIT_PATTERN)


# Functions for creating lines.


def end() -> Line:
    """Creates an end line."""
    return Line(END_LINE, "", "")


def text(info: str, content: str) -> Line:
    """Creates a text line."""
    return Line(TEXT_LINE, info, content)


def label(content: str) -> Line:
    """Creates a label line."""
    return Line(LABEL_LINE, "", content)


def jump(content: str) -> Line:
    """Creates a jump line."""
    return Line(JUMP_LINE, "", content)


def menu(info: str, content: str) -> Line:
    """Creates a menu line."""
    return Line(MENU_LINE, info, content)


def variable(info: str, content: str) -> Line:
    """Creates a variable line."""
    return Line(VARIABLE_LINE, info, content)


def check(content: str) -> Line:
    """Creates a check line."""
    return Line(CHECK_LINE, "", content)


def comment(content: str) -> Line:
    """Creates a comment line."""
    return Line(COMMENT_LINE, "", content)
