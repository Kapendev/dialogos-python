"""
A super simple dialogue system for Python.

This module contains all the structures and functions needed
to create a dialogue for a game.
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
VARIABLE_PATTERN = r"__(\w+)"
PROCEDURE_PATTERN = r"!!(\w+)\((\w*)\)"


class Line:
    """The dialogue line structure."""

    def __init__(self, t: int, info: str, content: str) -> None:
        """
        Creates a new line.

        Each line has a type and some information that defines how its content will be used by a system.
        """
        self.t = t
        self.info = info
        self.content = content

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
        self.index = 0
        self.lines: List[Line] = []
        self.labels: Dict[str, int] = {}
        self.variables: Dict[str, str] = {}
        self.procedures: Dict[str, Callable[[str], str]] = {}
        if lines is not None:
            self.change(lines)

    def __repr__(self) -> str:
        return "Dialogue(index: {}, lines: {}, labels: {}, variables: {})".format(
            self.index, self.lines, self.labels, self.variables
        )

    def line(self) -> Line:
        """Returns the current line of the dialogue."""

        def replace(s: str) -> str:
            result = s
            for match in re.finditer(VARIABLE_PATTERN, s):
                target = match.group()
                key = match.group(1)
                if key in self.variables:
                    result = result.replace(target, self.variables[key])
            s = result
            for match in re.finditer(PROCEDURE_PATTERN, s):
                target = match.group()
                key = match.group(1)
                arg = match.group(2)
                if key in self.procedures:
                    result = result.replace(target, self.procedures[key](arg))
            return result

        line = self.lines[self.index]
        return Line(line.t, replace(line.info), replace(line.content))

    def change(self, lines: List[Line]) -> None:
        """Changes the lines of the dialogue."""
        self.reset()
        self.labels.clear()
        self.lines = lines
        for i, line in enumerate(self.lines):
            if line.t == LABEL_LINE:
                self.labels[line.content] = i
        self.lines.append(end())
        self.update()

    def next(self) -> None:
        """Advances the index of the dialogue by one."""
        self.index += 1
        self.update()

    def jump(self, label: str) -> None:
        """Changes the index of the dialogue by using a label."""
        self.index = self.labels[label]
        self.update()

    def reset(self) -> None:
        """Resets the dialogue index."""
        self.index = 0

    def has_end(self) -> bool:
        """Returns true if the current line of the dialogue is an end line."""
        return self.lines[self.index].t == END_LINE

    def has_menu(self) -> bool:
        """Returns true if the current line of the dialogue is a menu line."""
        return self.lines[self.index].t == MENU_LINE

    def choices(self) -> List[str]:
        """Returns the choices of a menu line
        if the current line of the dialogue is a menu line.
        """
        line = self.line()
        if line.t == MENU_LINE:
            return split(line.content)
        return []

    def choose(self, choice: int) -> None:
        """Chooses a label from the current menu line and jumps to it."""
        self.jump(split(self.line().info)[choice])

    def update(self) -> None:
        """Updates the dialogue state."""
        line = self.line()
        if line.t == LABEL_LINE or line.t == COMMENT_LINE:
            self.next()
        elif line.t == JUMP_LINE:
            if line.content in self.labels:
                self.jump(line.content)
            else:
                self.next()
        elif line.t == VARIABLE_LINE:
            value = calc(line.content)
            if value is not None:
                self.variables[line.info] = str(value)
            else:
                self.variables[line.info] = line.content
            self.next()
        elif line.t == CHECK_LINE:
            value = calc(line.content)
            if value is not None and value != 0:
                self.next()
            else:
                self.index += 2
                if self.index >= len(self.lines):
                    self.index = len(self.lines) - 1
                self.update()


def calc(s: str) -> Optional[float]:
    """Parses and evaluates simple math expressions."""
    result: Optional[float] = None
    args = s.strip().split(" ")
    if len(args) >= 3:
        try:
            result = float(args[0])
            front = 0
            while front + 2 < len(args):
                op = args[front + 1]
                n2 = float(args[front + 2])
                if op == "+":
                    result += n2
                elif op == "-":
                    result -= n2
                elif op == "*":
                    result *= n2
                elif op == "/":
                    result /= n2
                elif op == "%":
                    result %= n2
                elif op == "<":
                    result = float(result < n2)
                elif op == ">":
                    result = float(result > n2)
                elif op == "<=":
                    result = float(result <= n2)
                elif op == ">=":
                    result = float(result >= n2)
                elif op == "==":
                    result = float(result == n2)
                elif op == "!=":
                    result = float(result != n2)
                else:
                    result = None
                    break
                front += 2
        except ValueError:
            result = None
    return result


def split(s: str) -> List[str]:
    """Splits a string with the dialogue split pattern."""
    return s.strip().split(SPLIT_PATTERN)


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
