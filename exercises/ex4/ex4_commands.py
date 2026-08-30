from ex4_turtle import TurtleState, TurtlePlot

### Helpers ####
def create_new_turtleplot(turtle_state: TurtleState, previous_pen_state: bool|None) -> bool:
    add_plot = False
    if turtle_state.cur_pen.pen_up == False:
        if len(turtle_state.turtle_plots) == 0:
            add_plot = True
        elif turtle_state.cur_pen.pen_type != turtle_state.turtle_plots[-1].pen_type:
            add_plot = True
        elif previous_pen_state is not None and previous_pen_state:
            add_plot = True

    if add_plot:
        turtle_state.turtle_plots.append(TurtlePlot(turtle_state))
        return True
    else:
        return False

def turtle_move(turtle_state: TurtleState, xy_new: tuple[int, int]) -> None:
    """Move turtle to a new position"""
    create_new_turtleplot(turtle_state, None)
    (turtle_state.cur_x, turtle_state.cur_y) = xy_new
    if not turtle_state.cur_pen.pen_up:
        turtle_state.turtle_plots[-1].draw_turtle(turtle_state.cur_x, turtle_state.cur_y, turtle_state.cur_pen.pen_up)

### Commands ###

def cmdSetPenStatus(turtle_state: TurtleState) -> None:
    """Set pen line style"""
    turtle_state.cur_pen.update_pen_type(turtle_state.cur_command[1])

def cmdPenDown(turtle_state: TurtleState) -> None:
    """Set pen in the drawing mode"""
    was_pen_up = turtle_state.cur_pen.pen_up
    turtle_state.cur_pen.pen_up_down(pen_up=False)
    if not create_new_turtleplot(turtle_state, was_pen_up):
        turtle_state.turtle_plots[-1].update_plot(turtle_state.cur_x, turtle_state.cur_y)

def cmdPenUp(turtle_state: TurtleState) -> None:
    """Set pen in the mode without drawing"""
    turtle_state.cur_pen.pen_up_down(pen_up=True)

def cmdMove(turtle_state: TurtleState, dx: int, dy: int) -> None:
    """Move turtle by (dx, dy) direction, scaled by step and command argument"""
    distance = turtle_state.step * int(turtle_state.cur_command[1])
    x_new = turtle_state.cur_x + dx * distance
    y_new = turtle_state.cur_y + dy * distance
    turtle_move(turtle_state, (x_new, y_new))

def cmdMoveEast(turtle_state: TurtleState) -> None:
    """Move turtle east"""
    cmdMove(turtle_state, 1, 0)

def cmdMoveWest(turtle_state: TurtleState) -> None:
    """Move turtle west"""
    cmdMove(turtle_state, -1, 0)

def cmdMoveNorth(turtle_state: TurtleState) -> None:
    """Move turtle north"""
    cmdMove(turtle_state, 0, 1)

def cmdMoveSouth(turtle_state: TurtleState) -> None:
    """Move turtle south"""
    cmdMove(turtle_state, 0, -1)

def cmdQuit(turtle_state) -> bool:
    """End receiveing commands"""
    return False

################