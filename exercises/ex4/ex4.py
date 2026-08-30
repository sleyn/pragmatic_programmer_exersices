from __future__ import annotations
import matplotlib.pyplot as plt
from ex4_commands import (
    cmdSetPenStatus, cmdPenDown, cmdPenUp,
    cmdMoveEast, cmdMoveWest, cmdMoveNorth, cmdMoveSouth, cmdQuit,
)
from ex4_turtle import TurtleState, Pen

# Each command has an value of tuple:
# (has argument: bool, dedicated function, [optional] accepted inputs)
ACCEPTED_PEN_STYLES = ("-", "--", "-.", ":")
ACCEPTED_COMMANDS = {
    "P": (True, cmdSetPenStatus, [str(i) for i in range(len(ACCEPTED_PEN_STYLES))]),
    "D": (False, cmdPenDown),
    "U": (False, cmdPenUp),
    "E": (True, cmdMoveEast),
    "W": (True, cmdMoveWest),
    "N": (True, cmdMoveNorth),
    "S": (True, cmdMoveSouth),
    "Q": (False, cmdQuit)
    }

def input_error():
    commands_with_arg =  [command for command in ACCEPTED_COMMANDS.keys() if ACCEPTED_COMMANDS[command][0]]
    commands_without_arg =  set(ACCEPTED_COMMANDS.keys()) - set(commands_with_arg)
    commands_with_list = [command for command in ACCEPTED_COMMANDS.keys() if len(ACCEPTED_COMMANDS[command]) == 3]
    print(
f"""
The valid input should be command from list:
{", ".join(ACCEPTED_COMMANDS.keys())}
{", ".join(commands_with_arg)} should have a value
{", ".join(commands_without_arg)} should not have a value\n
""" + \
"\n".join([f"Command '{command}' accepts values: {", ".join(ACCEPTED_COMMANDS[command][2])}" for command in commands_with_list])
    )

def is_input_valid(inputs_list, known_commands):
    if inputs_list[0] not in known_commands or len(inputs_list) != known_commands[inputs_list[0]][0] + 1:
        input_error()
        return False
    if len(known_commands[inputs_list[0]]) == 3 and inputs_list[1] not in known_commands[inputs_list[0]][2]:
        input_error()
        return False
    return True

def turtle_action(turtle_state: TurtleState) -> bool:
    if is_input_valid(turtle_state.cur_command, ACCEPTED_COMMANDS):
        command_out = ACCEPTED_COMMANDS[turtle_state.cur_command[0]][1](turtle_state)
        return command_out is None
    return True


if __name__ == "__main__":
    turtle_state = TurtleState(
        cur_command = [],
        cur_x=30,
        cur_y=30,
        cur_pen=Pen(pen_up=True, pen_type="0", accepted_styles=ACCEPTED_PEN_STYLES),
        step=10,
        turtle_plots = []
    )

    continue_loop = True

    while continue_loop:
        turtle_state.cur_command = input().split()
        continue_loop = turtle_action(turtle_state)

    for turtle_plot in turtle_state.turtle_plots:
        turtle_plot.plot()

    plt.show()
