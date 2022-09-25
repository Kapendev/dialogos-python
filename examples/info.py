from dialogos import *


def player(content: str) -> Line:
    return text("$p_name||$p_emo", content)


d = Dialogue(
    [
        player("Hmmm..."),
        player("Hm!"),
        variable("p_emo", "Yiik"),
        player("What is going on?"),
        variable("p_emo", "Happy"),
        player("Haha!"),
    ]
).add_variables({"p_name": "Ansley", "p_emo": "Neutral"})

while not d.has_end():
    line = d.line()
    data = split(line.info)
    name = data[0]
    emo = "😐" if data[1] == "Neutral" else "😮" if data[1] == "Yiik" else "😀"
    print("{} {}: {}".format(name, emo, line.content))
    d.next()
