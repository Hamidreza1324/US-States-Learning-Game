"""
U.S. States Learning Game
A simple interactive geography game where players guess U.S. states
and see their correct locations displayed on the map.
"""

import turtle
import pandas
import time

# ----------------------------------- #
#            CONFIGURATION            #
# ----------------------------------- #

IMAGE_PATH = "blank_states_img.gif"
DATA_PATH = "50_states.csv"


# ----------------------------------- #
#           SETUP SCREEN              #
# ----------------------------------- #

screen = turtle.Screen()
screen.title("U.S. States Learning Game")
screen.addshape(IMAGE_PATH)
turtle.shape(IMAGE_PATH)


# ----------------------------------- #
#           LOAD DATA                 #
# ----------------------------------- #

data = pandas.read_csv(DATA_PATH)
all_states = data.state.to_list()
guessed_states = []
start_time = time.time()


# ----------------------------------- #
#        UTILITY FUNCTIONS            #
# ----------------------------------- #

def write_state(name, x, y):
    """Writes the guessed state name on the map."""
    marker = turtle.Turtle()
    marker.hideturtle()
    marker.penup()
    marker.goto(x, y)
    marker.write(name, align="center", font=("Arial", 8, "bold"))


def show_score():
    """Displays score in the title bar."""
    screen.title(
        f"U.S. States Learning Game | Score: {len(guessed_states)}/50")


def get_hint():
    """Returns one unguessed state as hint."""
    for state in all_states:
        if state not in guessed_states:
            return state
    return None


# ----------------------------------- #
#           MAIN GAME LOOP            #
# ----------------------------------- #

show_score()

while len(guessed_states) < 50:
    answer = screen.textinput(
        title=f"{len(guessed_states)}/50 States Correct",
        prompt="Enter a state (or type 'Hint' / 'Exit'):"
    )

    if not answer:
        continue

    answer_state = answer.strip().title()

    if answer_state == "Exit":
        missing = [state for state in all_states if state not in guessed_states]
        pandas.DataFrame(missing).to_csv("states_to_learn.csv")
        break

    if answer_state == "Hint":
        hint = get_hint()
        if hint:
            turtle.clearscreen()
            screen.addshape(IMAGE_PATH)
            turtle.shape(IMAGE_PATH)
            print(f"Hint: Try '{hint}' 😉")
        continue

    if answer_state in all_states and answer_state not in guessed_states:
        guessed_states.append(answer_state)

        # Write state on map
        row = data[data.state == answer_state]
        write_state(answer_state, int(row.x), int(row.y))

        show_score()


# ----------------------------------- #
#           END MESSAGE               #
# ----------------------------------- #

end_time = int(time.time() - start_time)
turtle.clearscreen()
turtle.write(
    f"Great job!\nYou got {len(guessed_states)} states.\nTime: {end_time} seconds",
    align="center",
    font=("Arial", 14, "bold")
)

screen.exitonclick()
