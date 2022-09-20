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
    def __init__(self, t: int, info: str, content: str) -> None:
        self.t = t
        self.info = info
        self.content = content

    def __repr__(self) -> str:
        return "Line(t: {}, info: '{}', content: '{}')".format(
            self.t, self.info, self.content
        )


class Dialogue:
    def __init__(self, lines: List[Line]) -> None:
        self.index = 0
        self.lines: List[Line] = []
        self.labels: Dict[str, int] = {}
        self.variables: Dict[str, str] = {}
        self.procedures: Dict[str, Callable[[str], str]] = {}
        self.change(lines)

    def __repr__(self) -> str:
        return "Dialogue(index: {}, lines: {}, labels: {}, variables: {})".format(
            self.index, self.lines, self.labels, self.variables
        )

    def line(self) -> Line:
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
        self.reset()
        self.labels.clear()
        self.lines = lines
        for i, line in enumerate(self.lines):
            if line.t == LABEL_LINE:
                self.labels[line.content] = i
        self.lines.append(end())
        self.update()

    def next(self) -> None:
        self.index += 1
        self.update()

    def jump(self, label: str) -> None:
        self.index = self.labels[label]
        self.update()

    def reset(self) -> None:
        self.index = 0

    def has_end(self) -> bool:
        return self.lines[self.index].t == END_LINE

    def has_menu(self) -> bool:
        return self.lines[self.index].t == MENU_LINE

    def choices(self) -> List[str]:
        return split(self.line().content)

    def choose(self, choice: int) -> None:
        self.jump(split(self.line().info)[choice])

    def update(self) -> None:
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
    return s.strip().split(SPLIT_PATTERN)


def end() -> Line:
    return Line(END_LINE, "", "")


def text(info: str, content: str) -> Line:
    return Line(TEXT_LINE, info, content)


def label(content: str) -> Line:
    return Line(LABEL_LINE, "", content)


def jump(content: str) -> Line:
    return Line(JUMP_LINE, "", content)


def menu(info: str, content: str) -> Line:
    return Line(MENU_LINE, info, content)


def variable(info: str, content: str) -> Line:
    return Line(VARIABLE_LINE, info, content)


def check(content: str) -> Line:
    return Line(CHECK_LINE, "", content)


def comment(content: str) -> Line:
    return Line(COMMENT_LINE, "", content)
