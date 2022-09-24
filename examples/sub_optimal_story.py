from dialogos import *


def gregory(content: str) -> Line:
    return text("Gregory", content)

def narrator(content: str) -> Line:
    return text("Narrator", content)

def god(content: str) -> Line:
    return text("You", content)


d = Dialogue(
    [
        label("TOP"),
        narrator("This is the story of a man named Gregory. Gregory worked on a large corporation and today was a special day.He was chosen to pitch one of his ideas to the companies leaders. It was 9:30. He had a meeting at 10."),
        gregory("What should I do? (thought gregory)."),
        menu("TEETH||GO", "Brush my teeth.||Go to the meeting."),
        label("GO"),
        gregory("I should go the the pitch."),
        narrator("Gregory rammed throught the door and started running towards his office. He thought being early would make an impression but he sadly forgot that also beeing in your pijamas would also make an impression. Not a good one that is."),
        narrator("After he attended the meeting he heard people from the office laughing at him and how he was <too old to wear mickey mouse pijamas>.He was a sad, sappy sucker. He went home and slept the rest of the day.After waking up he thought to himself,could I have done something diferent?"),
        jump("BSIDE"),
        label("TEETH"),
        narrator("Gregory brushed his teeth squicky clean."),
        gregory("I still have 25 mins left. What now?"),
        narrator("said Gregory"),
        menu("SUIT||GO2||THINK", "Dress up.||Go to the meeting.||Think about life."),
        label("GO2"),
        narrator("Gregory rammed throught the door and started running towards his office. He thought being early would make an impression but he sadly forgot that also beeing in your pijamas would also make an impression. Not a good one that is."),
        narrator("After he attended the meeting he heard people from the office laughing at him and how he was <too old to wear mickey mouse pijamas>.He was a sad, sappy sucker. He went home and slept the rest of the day.After waking up he thought to himself,could I have done something diferent?"),
        jump("BSIDE"),
        label("SUIT"),
        narrator("Gregory wore the fanciest of the suits he had and then:"),
        menu("GO3||THINK", "Go to the meeting.||Think about life."),
        label("THINK"),
        gregory("What am I doing with my life?Is this where Ive come to? Who am I? Why am I here???"),
        narrator("Gregory was going mental! He had to calm down right?"),
        menu("NEXT||GO3", "No||Yes he should chill."),
        label("NEXT"),
        narrator("You want him to continue??? Are yoou mad???? I mean. *coughs*"),
        narrator("Gregory continued thinking."),
        gregory("Where do we go when we die?Why do we exist as a spieces?Does god exist? Do I exist?"),
        narrator("The time was 9:50. If he snapped out of it right now he would only be late by 5 mins. He could still make it!"),
        menu("NEXT2||GO4","No thou shall contineu||Ok enough messing around.Gregorius-Chillius"),
        label("NEXT2"),
        narrator("You are a mean MEAN person you hear me? Standing behind your screen laughing at an inocent man loosing his bloody shit! who do you think you are?People like you make me sick!"),
        narrator("I give you one. ONE last chance ti fix him."),
        gregory("What are we , where are we? You, up there . Yeah I am talking to you,the one behind the screen. What am I? Am I even real?Is this a clear ripoff of the critically aclaimed game <The Stanely Parable>?Please. I beg you. I know you are listening. Give me an answer."),
        menu("TRUTH||LIE", "Tell him the truth.||Lie about reality"),
        label("LIE"),
        god("Gregory Listen to me. You've been in a coma for the last 5 years.You need to wake up."),
        narrator("WHAT???? I GIVE YOU ONE MORE CHANCE AND THIS IS WHAT YOU DO WITH IT???"),
        gregory("Oh my god! I need to free myself from this coma!"),
        narrator("Look at him now!You made him clinically insane!You are a bad person you know that?You propably steal candy from kids as a hobby."),
        gregory("But how can I free myself from this prison my human body has created?"),
        narrator("You propably burn orphanages as a side hobby! You people discuss me."),
        gregory("I know! If this is a dream the If I die in the dream I will be free! I hear trafic coming from my front door."),
        narrator("You are propably behind 9... I sorry WHAT? Gregory NO DONT DO IT!"),
        gregory(" Real world here I come!"),
        narrator("Gregory NOOOOOO!!!"),
        narrator("Look at this! WHAT HAVE YOU DONE? Are you proud of yourself??"),
        menu("YES||NO", "Yes||No"),
        label("NO"),
        narrator("Yeah thats what I thougt.NOW I HAVE TO CLEAN THIS ALLA-"),
        narrator("Big breaths, dont let him get to you. Inhale. Exhale. Allright everyone from the top!"),
        label("YES"),
        narrator("You think you are funny? Now I have to clean this mess up!"),
        narrator("Give me a break.... Here we go from the top."),
        jump("TOP"),
        label("TRUTH"),
        god("You live in a simulation that is curently running on my computer.I will now make you forget so you can contineu on with your life."),
        gregory("WAIT NO"),
        jump("TOP"),
        label("GO4"),
        narrator("Gregory snapped out of it."),
        gregory("What am I doing? I have a meeting to atend!Get your shit together Greg!"),
        narrator("Gregory was 5 minitues late to the meeting.After a long apology he started with the pitch. The meeting went...fine . Nothing of note happened that day. Just a usual day for ol' Greg. At noon he went to the bar and thought to himself, could I have done something diferent?"),
        jump("BSIDE"),
        label("GO3"),
        narrator("Gregory went to the meeting right on time.The meeting was sucesful, Gregory earned a promotion. He thought to himself"),
        gregory("Life is really good now. But I wonder could I have done something diferent?"),
        label("BSIDE"),
        menu("END||TOP", "Nah||Go back"),
        end(),
        label("END"),
        narrator("Nah he thought to himself."),
        narrator("Thanks for playing my text adventure. This content was generated by Infdev."),
        end(),
    ]
)

while not d.has_end():
    while d.has_menu():
        print()
        for i, choice in enumerate(d.choices()):
            print("({}) => {}".format(i, choice))
        d.choose(int(input()))
    line = d.line()
    print("{}: {}".format(line.info, line.content))
    d.next()
