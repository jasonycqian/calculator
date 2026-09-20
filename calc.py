from graphics import *
import random
import math
from time import sleep


def draw_button(a, b, c):
    button = Circle(Point(a, b), c)
    button.setWidth(0)
    button.setFill(color_rgb(220, 210, 195))
    button.draw(win)


def label_button(a, b, c, d):
    buttondisplaysgrid = [
        ["\u221a", "ANS", "\u232B", "AC"],
        ["7", "8", "9", "\u00f7"],
        ["4", "5", "6", "\u00d7"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
    ]
    label = Text(Point(a, b), buttondisplaysgrid[c][d])
    label.setSize(30)
    label.draw(win)
    return buttondisplaysgrid[c][d]


win = GraphWin("Calculator", 512, 768, autoflush=False)
bg = Rectangle(Point(0, 0), Point(512, 768))
bg.setFill(color_rgb(0, 0, 0))
bg.draw(win)

display = Rectangle(Point(32, 32), Point(480, 256))
display.setWidth(8)
display.setOutline(color_rgb(255, 0, 0))
display.setFill(color_rgb(220, 210, 195))
display.draw(win)

display_text = Text(Point(55, 70), "")
display_text.setSize(36)
display_text.setStyle("bold")
display_text.draw(win)

result_text = Text(Point(300, 200), "")
result_text.setSize(36)
result_text.setStyle("bold")
result_text.draw(win)

buttons = []
button_radius = 36
for row in range(5):
    for col in range(4):
        x_buttongrid = 82 + (col * 116)
        y_buttongrid = 320 + (row * 96)
        draw_button(x_buttongrid, y_buttongrid, button_radius)
        button_symbol = label_button(x_buttongrid, y_buttongrid, row, col)
        buttons.append(
            {"x": x_buttongrid, "y": y_buttongrid, "label": button_symbol}
        )

update()

current_input = ""
current_output = ""
input_lock = False
prev_ans = ""
while True:
    click = win.getMouse()
    if click is None:
        continue
    for btn in buttons:
        dx = click.getX() - btn["x"]
        dy = click.getY() - btn["y"]
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= button_radius:
            key = btn["label"]
            if current_output == "Math ERROR" and key != "AC":  # only allows AC key if Math ERROR
                pass

            elif input_lock == True and not (
                key in ["AC", "\u00d7", "\u00f7", "+", "-", "ANS"]
            ):
                pass

            elif key == "AC":  # clears the input, clears the output
                current_input = ""
                current_output = ""
                input_lock = False

            elif key == "\u221a":  # sqrt; locks input, gives an output
                try:
                    expr = (
                        current_input.replace("\u00d7", "*")
                        .replace("\u00f7", "/")
                        .replace("ANS", prev_ans)
                    )
                    val = float(eval(expr))
                    if val < 0:
                        current_output = "Math ERROR"
                    else:
                        res = math.sqrt(val)
                        if res.is_integer():
                            current_output = str(int(res))  # Turns √25 -> 5.0 -> "5"
                        else:
                            current_output = str(
                                round(res, 6)
                            )  # Keeps √2 -> "1.414214"
                        current_input = "\u221a(" + current_input + ")"
                        input_lock = True
                        prev_ans = current_output
                except Exception:
                    current_output = "Math ERROR"

            elif key == "ANS":  # adds ANS to the end of the input
                if input_lock == True:
                    current_output = ""
                    current_input = "ANS"
                    input_lock = False
                else:
                    current_input += "ANS"

            elif key == "\u232B":
                if current_input.endswith("ANS"):
                    current_input = current_input[:-3]
                else:
                    current_input = current_input[:-1]

            elif key == "=":
                try:
                    expr = (
                        current_input.replace("\u00d7", "*")
                        .replace("\u00f7", "/")
                        .replace("ANS", prev_ans)
                    )
                    val = eval(expr)
                    if isinstance(val, float) and val.is_integer():
                        current_output = str(int(val))
                    else:
                        current_output = str(round(val, 6))
                    prev_ans = current_output
                    input_lock = True
                except Exception:
                    current_output = "Math ERROR"

            elif key == "\u00d7" or key == "\u00f7" or key == "+" or key == "-":
                if input_lock == True:
                    current_output = ""
                    current_input = "ANS"
                    input_lock = False
                current_input += key

            else:  # must have clicked 1234567890. so add to the end of input
                current_input += key

            display_text.setText(current_input)
            result_text.setText(current_output)

            target_x_input = 55 + (len(current_input) * 20 / 2)
            current_x_input = display_text.getAnchor().getX()
            display_text.move(target_x_input - current_x_input, 0)

            target_x_output = 455 - (len(current_output) * 20 / 2)
            current_x_output = result_text.getAnchor().getX()
            result_text.move(target_x_output - current_x_output, 0)

            update()
            break