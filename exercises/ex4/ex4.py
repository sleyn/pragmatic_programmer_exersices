import matplotlib.pyplot as plt

ACCEPTED_COMMANDS = ("P", "D", "U", "E", "W", "N", "S", "Q")

def input_error():
    print(
f"""
The valid input should be command from list:
{", ".join(ACCEPTED_COMMANDS)}
P, E, W, N, S should have a value
D, U, Q should not have a value
"""
    )


class TurtlePlot():
    def __init__(
            self,
            step: int = 10,
            x_start: int = 30,
            y_start: int = 30,
            pen_type = "0"
            ):
        self.x_points = [x_start]
        self.y_points = [y_start]
        self.step = step
        self.pen_type = self.select_pen(pen_type)

    def add_step(self, command: str, value: str, is_pen_up) -> tuple[int, int]:
        int_value = int(value)
        match command:
            case "S":
                return self.move_turtle(0, -self.step * int_value, is_pen_up)
            case "N":
                return self.move_turtle(0, self.step * int_value, is_pen_up)
            case "W":
                return self.move_turtle(-self.step * int_value, 0, is_pen_up)
            case "E":
                return self.move_turtle(self.step * int_value, 0, is_pen_up)
            case _:
                raise ValueError(f"Unsupported movement command: {command}")


    def move_turtle(self, x_update, y_update, is_pen_up) -> tuple[int, int]:
        if not is_pen_up:
            self.update_plot(x_update, y_update)
        return self.x_points[-1] + x_update, self.y_points[-1] + y_update
            

    def update_plot(self, x_update, y_update):
        self.x_points.append(self.x_points[-1] + x_update)
        self.y_points.append(self.y_points[-1] + y_update)

    def select_pen(self, pen_type: str):
        """Solid, Dashed, Dash-dot, Dotted"""
        self.pen_type = ["-", "--", "-.", ":"][int(pen_type)]

    def plot(self):
        plt.plot(
            self.x_points, self.y_points,
            ls=self.pen_type,
            color='blue'
        )


if __name__ == "__main__":
    turtle_plots: list[TurtlePlot]  = list()
    current_pen = "0"
    pen_up = True
    cur_x = 30
    cur_y = 30

    while True:
        parts: list = input().split()
        input_error() if parts[0] not in ACCEPTED_COMMANDS else None

        if parts[0] == "Q":
            break

        if parts[0] in ("E", "W", "N", "S"):
            if len(parts) == 2:
                cur_x, cur_y = turtle_plots[-1].add_step(parts[0], parts[1], pen_up)
            else:
                input_error()

        if parts[0] == "P":
            if len(parts) == 2:
                 current_pen = parts[1]
            else:
                input_error()

        if parts[0] in ("D", "U"):
            pen_up = parts[0] == "U"
            if parts[0] == "U" and len(turtle_plots) > 0:
                cur_x = turtle_plots[-1].x_points[-1]
                cur_y = turtle_plots[-1].y_points[-1]
            if parts[0] == "D":
                turtle_plots.append(TurtlePlot(x_start=cur_x, y_start=cur_y, pen_type=current_pen))


    for turtle_plot in turtle_plots:
        turtle_plot.plot()

    plt.show()
