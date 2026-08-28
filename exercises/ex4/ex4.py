from __future__ import annotations
import matplotlib.pyplot as plt
from dataclasses import dataclass
from copy import deepcopy

ACCEPTED_COMMANDS = ("P", "D", "U", "E", "W", "N", "S", "Q")
ACCEPTED_PEN_STYLES = ("-", "--", "-.", ":")


class Pen:
    def __init__(self, pen_up: bool = True, pen_type: str = "0"):
        self.pen_up: bool = True
        self.pen_up_down(pen_up)
        self.pen_type: str = self.select_pen(pen_type)

    def update_pen_type(self, pen_type: str) -> None:
        self.pen_type = self.select_pen(pen_type)

    @staticmethod
    def select_pen(pen_type: str) -> str:
            """Solid, Dashed, Dash-dot, Dotted"""
            return ACCEPTED_PEN_STYLES[int(pen_type)]

    def pen_up_down(self, pen_up: bool) -> None:
        self.pen_up = pen_up


@dataclass
class TurtleState:
    cur_x: int
    cur_y: int
    cur_pen: Pen
    step: int

    def snapshot(self) -> TurtleState:
        return deepcopy(self)

class TurtlePlot():
    def __init__(
            self,
            turtle_state: TurtleState = TurtleState(
                cur_x=30, 
                cur_y=30, 
                step=10, 
                cur_pen=Pen(pen_up=True, pen_type="0")
                )
            ):
        self.pen_type: str = turtle_state.cur_pen.pen_type
        self.x_points: list[int] = []
        self.y_points: list[int] = []
        if not turtle_state.cur_pen.pen_up:
            self.update_plot(turtle_state.cur_x, turtle_state.cur_y)

    def add_step(self, command: str, value: str, turtle_state: TurtleState) -> tuple[int, int]:
        int_value = int(value)
        match command:
            case "S":
                x_new = turtle_state.cur_x
                y_new = turtle_state.cur_y - turtle_state.step * int_value
            case "N":
                x_new = turtle_state.cur_x
                y_new = turtle_state.cur_y + turtle_state.step * int_value
            case "W":
                x_new = turtle_state.cur_x - turtle_state.step * int_value
                y_new = turtle_state.cur_y
            case "E":
                x_new = turtle_state.cur_x + turtle_state.step * int_value
                y_new = turtle_state.cur_y
            case _:
                raise ValueError(f"Unsupported movement command: {command}")
        self.move_turtle(x_new, y_new, turtle_state.cur_pen.pen_up)
        return x_new, y_new

    def move_turtle(self, x_new, y_new, is_pen_up) -> None:
        if not is_pen_up:
            self.update_plot(x_new, y_new)

    def last_turtle_position(self) -> tuple[int, int]:
        return self.x_points[-1], self.y_points[-1]

    def update_plot(self, x_new, y_new) -> None:
        self.x_points.append(x_new)
        self.y_points.append(y_new)

    def plot(self) -> None:
        plt.plot(
            self.x_points, self.y_points,
            ls=self.pen_type,
            color='blue'
        )

def create_new_turtleplot(turtle_plots: list[TurtlePlot], turtle_state: TurtleState, previous_state: TurtleState|None) -> bool:
    add_plot = False
    if turtle_state.cur_pen.pen_up == False:
        if turtle_state.cur_pen.pen_type != turtle_plots[-1].pen_type:
            add_plot = True
        elif previous_state is not None and previous_state.cur_pen.pen_up:
            add_plot = True

    if add_plot:
        turtle_plots.append(TurtlePlot(turtle_state))
        return True
    else:
        return False

def input_error():
    print(
f"""
The valid input should be command from list:
{", ".join(ACCEPTED_COMMANDS)}
P, E, W, N, S should have a value
D, U, Q should not have a value

Accepted P values: {", ".join(map(str, range(len(ACCEPTED_PEN_STYLES))))} correstponding to {", ".join(ACCEPTED_PEN_STYLES)}
"""
    )

def is_input_valid(inputs_list, n_expected):
    if len(inputs_list) != n_expected or inputs_list[0] not in ACCEPTED_COMMANDS:
        input_error()
        return False
    if inputs_list[0] == "P" and int(inputs_list[1]) not in range(len(ACCEPTED_PEN_STYLES)): return False
    return True

def turtle_action(parts: list, turtle_plots: list[TurtlePlot], turtle_state: TurtleState) -> bool:
    input_error() if parts[0] not in ACCEPTED_COMMANDS else None

    match parts[0]:
        case "Q":
            return False
        case "E" | "W" | "N" | "S":
            if not is_input_valid(parts, 2): return True
            create_new_turtleplot(turtle_plots, turtle_state, None)
            turtle_state.cur_x, turtle_state.cur_y = turtle_plots[-1].add_step(parts[0], parts[1], turtle_state)
        case "P":
            if not is_input_valid(parts, 2): return True
            turtle_state.cur_pen.update_pen_type(parts[1])
        case "U":
            turtle_state.cur_pen.pen_up_down(pen_up=True)
        case "D":
            previous_state = turtle_state.snapshot()
            turtle_state.cur_pen.pen_up_down(pen_up=False)
            if not create_new_turtleplot(turtle_plots, turtle_state, previous_state):
                turtle_plots[-1].update_plot(turtle_state.cur_x, turtle_state.cur_y)

    return True


if __name__ == "__main__":
    turtle_state = TurtleState(
        cur_x=30,
        cur_y=30,
        cur_pen=Pen(pen_up=True, pen_type="0"),
        step=10
    )
    turtle_plots: list[TurtlePlot]  = [TurtlePlot(turtle_state)]

    continue_loop = True

    while continue_loop:
        parts: list = input().split()
        continue_loop = turtle_action(parts, turtle_plots, turtle_state)

    for turtle_plot in turtle_plots:
        turtle_plot.plot()

    plt.show()
