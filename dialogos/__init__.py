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

    def add_variables(self, variables: Dict[str, str]) -> "Dialogue":
        """Adds new variables to the dialogue."""
        self.__variables.update(variables)
        return self

    def add_procedures(self, procedures: Dict[str, Callable[[str], str]]) -> "Dialogue":
        """Adds new procedures to the dialogue."""
        self.__procedures.update(procedures)
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

    def change_variables(self, variables: Dict[str, str]) -> "Dialogue":
        """Changes the variables of the dialogue."""
        self.__variables = variables
        return self

    def change_procedures(
        self, procedures: Dict[str, Callable[[str], str]]
    ) -> "Dialogue":
        """Changes the procedures of the dialogue."""
        self.__procedures = procedures
        return self

    def change_lines(self, lines: List[Line]) -> "Dialogue":
        """Changes the lines of the dialogue."""
        self.__labels.clear()
        self.__lines = lines
        for i, line in enumerate(self.__lines):
            if line.t == LABEL_LINE:
                self.__labels[line.content] = i
        self.__lines.append(end())
        self.reset()
        return self

    def line(self) -> Line:
        """Returns the current line of the dialogue."""

        def replace(s: str) -> str:
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

        line = self.__lines[self.__index]
        return Line(line.t, replace(line.info), replace(line.content))

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

    def __update(self) -> None:
        """Updates the dialogue state."""
        # Calling update should not call procedures
        # when a text line is processed.
        line = self.__lines[self.__index]
        if line.t != TEXT_LINE:
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
            if value is not None and value != 0.0:
                self.next()
            else:
                self.goto(self.__index + 2)


def calc(s: str) -> Optional[float]:
    """Parses and evaluates simple math expressions."""
    result: Optional[float] = None
    args = s.replace(" ", "")
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
