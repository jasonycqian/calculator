from graphics import *
import math

# --- Window & Grid Setup ---
WIDTH, HEIGHT = 448, 224
X_MIN, X_MAX = -10, 10
Y_MIN, Y_MAX = -10, 10


def math_to_screen(x, y):
    """Converts Cartesian (x, y) coordinates to pixel Point(px, py)."""
    px = (x - X_MIN) / (X_MAX - X_MIN) * WIDTH
    py = HEIGHT - ((y - Y_MIN) / (Y_MAX - Y_MIN) * HEIGHT)
    return Point(px, py)


def draw_axes_and_labels(win):
    """Draws X/Y axes, tick marks, and coordinate numbers."""
    origin = math_to_screen(0, 0)

    # Main X-Axis
    x_axis = Line(Point(0, origin.getY()), Point(WIDTH, origin.getY()))
    x_axis.setFill("gray")
    x_axis.draw(win)

    # Main Y-Axis
    y_axis = Line(Point(origin.getX(), 0), Point(origin.getX(), HEIGHT))
    y_axis.setFill("gray")
    y_axis.draw(win)

    # X-Axis Ticks & Labels
    for x in range(X_MIN, X_MAX + 1):
        if x == 0:
            continue  # Skip origin to avoid overlap
        pt = math_to_screen(x, 0)

        # Tick mark
        tick = Line(Point(pt.getX(), pt.getY() - 4), Point(pt.getX(), pt.getY() + 4))
        tick.draw(win)

        # Label text
        lbl = Text(Point(pt.getX(), pt.getY() + 15), str(x))
        lbl.setSize(8)
        lbl.setFill("darkgray")
        lbl.draw(win)

    # Y-Axis Ticks & Labels
    for y in range(Y_MIN, Y_MAX + 1):
        if y == 0:
            continue
        pt = math_to_screen(0, y)

        # Tick mark
        tick = Line(Point(pt.getX() - 4, pt.getY()), Point(pt.getX() + 4, pt.getY()))
        tick.draw(win)

        # Label text
        lbl = Text(Point(pt.getX() - 15, pt.getY()), str(y))
        lbl.setSize(8)
        lbl.setFill("darkgray")
        lbl.draw(win)


def safe_eval(expr, x_val):
    """Evaluates the string equation safely with Python's math module."""
    # Context dictionary exposes math functions (sin, cos, sqrt, etc.) and 'x'
    allowed_context = {
        "x": x_val,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "abs": abs,
        "pi": math.pi,
        "e": math.e,
    }
    return eval(expr, {"__builtins__": None}, allowed_context)


def plot_equation(win, expr_str, line_objects):
    """Erase old function lines and plot the new equation string."""
    # Undraw previous graph lines
    for line in line_objects:
        line.undraw()
    line_objects.clear()

    prev_pt = None
    num_steps = WIDTH

    for step in range(num_steps):
        x = X_MIN + (step / num_steps) * (X_MAX - X_MIN)

        try:
            y = safe_eval(expr_str, x)

            if y < Y_MIN or y > Y_MAX or type(y) is complex:
                prev_pt = None
                continue

            curr_pt = math_to_screen(x, y)

            if prev_pt:
                segment = Line(prev_pt, curr_pt)
                segment.setFill("blue")
                segment.setWidth(2)
                segment.draw(win)
                line_objects.append(segment)

            prev_pt = curr_pt

        except (ValueError, ZeroDivisionError, TypeError, SyntaxError):
            prev_pt = None


def draw():
    win = GraphWin("Graphing Calculator", WIDTH, HEIGHT)
    win.setBackground("white")

    draw_axes_and_labels(win)


    # Equation Entry Box
    lbl_eq = Text(Point(100, 30), "f(x) =")
    lbl_eq.setStyle("bold")
    lbl_eq.draw(win)

    entry_box = Entry(Point(250, 30), 25)
    entry_box.setText("x**2 - 4")  # Default equation
    entry_box.draw(win)

    # Plot Button Visual
    btn_box = Rectangle(Point(360, 15), Point(420, 45))
    btn_box.setFill("lightgray")
    btn_box.draw(win)

    btn_text = Text(Point(390, 30), "Plot")
    btn_text.setStyle("bold")
    btn_text.draw(win)


    drawn_lines = []

    # Initial plot
    plot_equation(win, entry_box.getText(), drawn_lines)

    # Wait for mouse clicks on the Plot button
    while True:
        click_pt = win.checkMouse()

        if click_pt:
            # Check if click landed inside the 'Plot' button boundary
            if 360 <= click_pt.getX() <= 420 and 15 <= click_pt.getY() <= 45:
                user_expr = entry_box.getText()
                plot_equation(win, user_expr, drawn_lines)

        # Check for keyboard Enter key press
        key = win.checkKey()
        if key == "Return":
            user_expr = entry_box.getText()
            plot_equation(win, user_expr, drawn_lines)

    win.close()


if __name__ == "__main__":
    draw()