from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy
import matplotlib.pyplot as plt

class Pen:
    def __init__(self, pen_up: bool = True, pen_type: str = "0", accepted_styles: tuple[str, ...] = ()):
        self.pen_up_down(pen_up)
        self.accepted_styles = accepted_styles
        self.pen_type: str = self.select_pen(pen_type)

    def update_pen_type(self, pen_type: str) -> None:
        self.pen_type = self.select_pen(pen_type)

    def select_pen(self, pen_type: str) -> str:
            """Solid, Dashed, Dash-dot, Dotted"""
            return self.accepted_styles[int(pen_type)]

    def pen_up_down(self, pen_up: bool) -> None:
        self.pen_up = pen_up

@dataclass
class TurtleState:
    cur_command: list[str]
    cur_x: int
    cur_y: int
    cur_pen: Pen
    step: int
    turtle_plots: list[TurtlePlot]


class TurtlePlot():
    def __init__(self, turtle_state: TurtleState):
        self.pen_type: str = turtle_state.cur_pen.pen_type
        self.x_points: list[int] = []
        self.y_points: list[int] = []
        if not turtle_state.cur_pen.pen_up:
            self.update_plot(turtle_state.cur_x, turtle_state.cur_y)

    def draw_turtle(self, x_new, y_new, is_pen_up) -> None:
        if not is_pen_up:
            self.update_plot(x_new, y_new)

    def update_plot(self, x_new, y_new) -> None:
        self.x_points.append(x_new)
        self.y_points.append(y_new)

    def plot(self) -> None:
        plt.plot(
            self.x_points, self.y_points,
            ls=self.pen_type,
            color='blue'
        )