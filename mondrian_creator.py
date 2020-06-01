"""
file = mondrian_creator.py

a random art generator in the style of Piet Mondrian
-creates the art
-gives the art a random name and displays it below the art
-includes a button at the bottom to let you reset and make another work of art
-includes a button which allows you to save a copy of your art


"""

import tkinter
from tkinter import *
import random
from PIL import ImageGrab
import PIL
import datetime

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 550
NUM_COLUMNS = 8
NUM_ROWS = 8
MASTER_WHITE = "gray98"
MASTER_BLACK = "black"
MASTER_BLUE = "blue3"
MASTER_YELLOW = "gold2"
MASTER_RED = "red3"
NUM_HORIZONTAL_SPLIT_MAX = 5
NUM_VERTICAL_SPLIT_MAX = 5

# Range from 1-10
BLUE_CHANCE = 3
YELLOW_CHANCE = 3
BLACK_CHANCE = 1


def main():
    # create the canvas, leaving enough room for the title at the bottom
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Mondrian Creator')
    run_art_creation_from_start(canvas)


# Essentially the main function. This is re-run when you click "create art"
def run_art_creation_from_start(canvas):
    # create one row of rectangles. Same height, random width. Let's start with 8.
    canvas.create_rectangle(7, 7, CANVAS_WIDTH - 2, CANVAS_WIDTH - 2, outline="black")
    list_of_colors_used = []
    list_of_x_values = create_list_of_random_widths()
    list_of_y_values = create_list_of_random_heights()
    x_values_used = []
    y_values_used = []
    num_sq_drawn = []
    list_of_objects = []
    draw_art(list_of_x_values, list_of_y_values, canvas, list_of_colors_used, x_values_used, y_values_used,
             num_sq_drawn, list_of_objects)
    draw_sub_squares_horizontal(list_of_x_values, list_of_y_values, canvas)
    draw_sub_squares_vertical(list_of_x_values, list_of_y_values, canvas)
    find_perfect_square(list_of_x_values, list_of_y_values, canvas, list_of_colors_used, x_values_used, y_values_used,
                        num_sq_drawn, list_of_objects)
    draw_large_squares(list_of_x_values, list_of_y_values, canvas, list_of_colors_used, x_values_used, y_values_used,
                       num_sq_drawn, list_of_objects)
    title = create_title(canvas, list_of_colors_used, num_sq_drawn)
    button(canvas, title)

    canvas.mainloop()


# creates the buttons
def button(canvas, title):
    b = Button(canvas, text="CREATE ART", command=lambda: restart_button(canvas, b, c))
    b.place(x=10, y=CANVAS_HEIGHT - 40)
    c = Button(canvas, text="SAVE", command=lambda: hide_me(canvas, b, c, title))
    c.place(x=95, y=CANVAS_HEIGHT - 40)


# the action which results from pressing the restart button. Clears the canvas and runs the program again
def restart_button(canvas, b, c):
    c.place_forget()
    b.place_forget()
    canvas.delete("all")
    run_art_creation_from_start(canvas)


# to hide buttons when taking a screen shot
def hide_me(canvas, b, c, title):
    c.place_forget()
    b.place_forget()
    canvas.after(1, lambda: timer(title, canvas))


# timer for how long the buttons should be hidden so they don't appear in the screenshot
def timer(title, canvas):
    canvas.after(1, lambda: save(title, canvas))


# Module to save a screenshot of your masterpiece
def save(title, canvas):
    now = datetime.datetime.now()
    date_time = now.strftime("%m-%d-%Y, %H%M%S")
    img = PIL.ImageGrab.grab(bbox=(441, 35, 940, 569))
    img.save("Masterpieces/" + title + " - " + str(date_time) + '.png', 'png')
    button(canvas, title)


# ensure that plain color names are displayed in title of the work of art
def color_name_fix(alist):
    for i in range(len(alist)):
        if alist[i] == MASTER_WHITE:
            alist[i] = "white"
        elif alist[i] == MASTER_BLACK:
            alist[i] = "black"
        elif alist[i] == MASTER_YELLOW:
            alist[i] = "yellow"
        elif alist[i] == MASTER_BLUE:
            alist[i] = "blue"
        elif alist[i] == MASTER_RED:
            alist[i] = "red"
    return alist


# creates a random title based on the colors used in the work of art
def create_title(canvas, list_of_colors_used, num_sq_drawn):
    number = random.randint(1, 99)
    # create string list:
    color_name_fix(list_of_colors_used)
    color_string = ""
    for color in list_of_colors_used:
        color_string = color_string + color
    if len(list_of_colors_used) == 0:
        # Draw from random list of names
        title = str("Grid no. %d" % number)
    elif len(list_of_colors_used) == 1:
        odds = random.randint(0, 2)
        # only if one square is run....
        if list_of_colors_used[0] == "red":
            title = str("Composition with red plane no. %d" % number)
        elif len(num_sq_drawn) == 1:
            title = str("Composition with " + list_of_colors_used[0] + " patch no. %d" % number)
        else:
            title = str("Composition with " + list_of_colors_used[0] + " no. %d" % number)
            # print(list_of_colors_used)
    elif len(list_of_colors_used) == 2:
        title = str(
            "Composition with " + list_of_colors_used[0] + " and " + list_of_colors_used[1] + " no. %d" % number)
    elif len(list_of_colors_used) >= 3:
        title = str("Composition with " + list_of_colors_used[0] + ", " + list_of_colors_used[1] + ", and " +
                    list_of_colors_used[2] + " no. %d" % number)
    canvas.create_text(CANVAS_WIDTH - 3, CANVAS_HEIGHT - 35, anchor="e", text=title, font=14)
    # print(list_of_colors_used)
    return title


# draws a random number of smaller squares horizontally
def draw_sub_squares_horizontal(list_x, list_y, canvas):
    number = random.randrange(0, NUM_HORIZONTAL_SPLIT_MAX)
    x_length = len(list_x)
    y_length = len(list_y)
    for i in range(number):
        rand_max = min(x_length, y_length)
        rand_x = random.randrange(0, rand_max - 1)
        x1 = list_x[rand_x]
        y1 = list_y[rand_x]
        x2 = ((list_x[rand_x + 1] - list_x[rand_x]) // 2) + list_x[rand_x]
        y2 = (list_y[rand_x + 1])
        canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=5,
                                fill=MASTER_WHITE)


# draws a random number of smaller squares vertically
def draw_sub_squares_vertical(list_x, list_y, canvas):
    number = random.randrange(0, NUM_VERTICAL_SPLIT_MAX)
    x_length = len(list_x)
    y_length = len(list_y)
    for i in range(number):
        rand_max = min(x_length, y_length)
        rand_x = random.randrange(0, rand_max - 1)
        x1 = list_x[rand_x]
        y1 = list_y[rand_x]
        x2 = (list_x[rand_x + 1])
        y2 = ((list_y[rand_x + 1] - list_y[rand_x]) // 2) + list_y[rand_x]
        canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=5,
                                fill=MASTER_WHITE)


# if close to a perfect square exists in the grid over three lines, make that and draw it red
# only draws one perfect square
def find_perfect_square(list_x, list_y, canvas, list_of_colors_used, x_values_used, y_values_used, num_sq_drawn,
                        list_of_objects):
    len_x = len(list_x)
    len_y = len(list_y)
    one_red_drawn = 0
    for i in range(1, len_x - 2):
        for j in range(1, len_y - 2):
            length_of_large_side = list_x[i + 2] - list_x[i]
            height_of_large_side = list_y[j + 2] - list_y[j]
            height_range_lower = height_of_large_side - 5
            height_range_upper = height_of_large_side + 5
            x = list_x[i]
            y = list_y[j]
            x2 = list_x[i + 2]
            y2 = list_y[j + 2]
            colliding_list = canvas.find_overlapping(x, y, x2, y2)
            if height_range_lower <= length_of_large_side <= height_range_upper:
                if one_red_drawn != 1:
                    collide_result = any(item in colliding_list for item in list_of_objects)
                    if not collide_result:
                        rectangle = canvas.create_rectangle(x, y, x2, y2, outline="black", width=5,
                                                            fill=MASTER_RED)
                        color = MASTER_RED
                        colors_used_list(color, list_of_colors_used)
                        num_sq_drawn.append(color)
                        values_used_add(x_values_used, y_values_used, x, x2, y, y2)
                        list_of_objects.append(rectangle)
                        one_red_drawn = 1
                        break
                    # else:
                    # print("overlap averted")


# draws a random number of larger rectangles. Makes sure they do not overlap the regular squares or the red square
def draw_large_squares(list_of_x_values, list_of_y_values, canvas, list_of_colors_used, x_values_used, y_values_used,
                       num_sq_drawn, list_of_objects):
    random_num = random.randrange(2, 6)
    one_big_drawn = 0
    for i in range(random_num):
        num_x = len(list_of_x_values)
        num_y = len(list_of_y_values)
        if num_x >= 5 and num_y >= 5:
            random_x = random.randrange(1, num_x - 2)
            random_y = random.randrange(1, num_y - 2)
            random_color = random.choice([MASTER_BLUE, MASTER_YELLOW])
            x = list_of_x_values[random_x - 1]
            y = list_of_y_values[random_y - 1]
            x2 = list_of_x_values[random_x + 2]
            y2 = list_of_y_values[random_y + 2]
            x_list_length = len(x_values_used)
            y_list_length = len(y_values_used)
            colliding_list = canvas.find_overlapping(x, y, x2, y2)
            # if x and x2 and y and y2 are not in the x_values_used, y_values_used
            for k in range(x_list_length):
                for l in range(y_list_length):
                    if not x <= x_values_used[k] <= x2:
                        if not x <= y_values_used[l] <= x2:
                            if not y <= y_values_used[l] <= y2:
                                if not y <= x_values_used[k] <= y2:
                                    if one_big_drawn != random_num:
                                        collide_result = any(item in colliding_list for item in list_of_objects)
                                        if not collide_result:
                                            colors_used_list(random_color, list_of_colors_used)
                                            rectangle = canvas.create_rectangle(x, y, x2, y2, outline="black", width=5,
                                                                                fill=random_color)
                                            num_sq_drawn.append(random_color)
                                            list_of_objects.append(rectangle)
                                            values_used_add(x_values_used, y_values_used, x, x2, y, y2)
                                            # print("big square")
                                            one_big_drawn += 1
                                        # else:
                                        # print("overlap averted")


# takes the random x coordinates and random y coordinates and makes rectangles using them.
# this makes the grid and randomly colors the regular sized rectangles
def draw_art(list_of_x_values, list_of_y_values, canvas, list_of_colors_used, x_values_used, y_values_used,
             num_sq_drawn, list_of_objects):
    for i in range(len(list_of_x_values) - 1):
        for j in range(len(list_of_y_values) - 1):
            x = list_of_x_values[i]
            y = list_of_y_values[j]
            x2 = list_of_x_values[i + 1]
            y2 = list_of_y_values[j + 1]
            random_color = find_random_color()
            colors_used_list(random_color, list_of_colors_used)
            rectangle = canvas.create_rectangle(x, y, x2, y2, outline="black", width=5, fill=random_color)
            if random_color != MASTER_WHITE:
                values_used_add(x_values_used, y_values_used, x, x2, y, y2)
                list_of_objects.append(rectangle)
                num_sq_drawn.append(random_color)
    # return x_values_used, y_values_used


# keeps track of which coordinates are use to create colored rectangles. Used to help prevent red square overlap
def values_used_add(x_values_used, y_values_used, x, x2, y, y2):
    if x not in x_values_used:
        x_values_used.append(x)
    if x2 not in x_values_used:
        x_values_used.append(x2)
    if y not in y_values_used:
        y_values_used.append(y)
    if y2 not in y_values_used:
        y_values_used.append(y2)


# used for title to help keep track of which blue, yellow, and red are used
def colors_used_list(color, list_of_colors_used):
    if color != MASTER_BLACK:
        if color != MASTER_WHITE:
            if color not in list_of_colors_used:
                list_of_colors_used.append(color)
    # return list_of_colors_used


# used to determine the color of the rectangles in the initial grid of rectangles. Most are simply white
def find_random_color():
    random_num = int(random.randrange(0, 100))
    black_odds = int(BLACK_CHANCE + 50)
    yellow_odds = int(YELLOW_CHANCE + 60)
    blue_odds = int(BLUE_CHANCE + 70)
    if 50 <= random_num <= black_odds:
        color = MASTER_BLACK
    elif 60 <= random_num <= yellow_odds:
        color = MASTER_YELLOW
    elif 70 <= random_num <= blue_odds:
        color = MASTER_BLUE
    else:
        color = MASTER_WHITE
    return color


# creates a list of the y coordinates for the initial grid of rectangles
def create_list_of_random_widths():
    # chooses a random number in a range and that is the number of columns...?
    # I guess that isn't necessary?
    # use the loop from above and save the values in a list. entry += 1
    # then use these when creating a bunch of rows, which will be of a random amount of heights
    canvas_frame_width = CANVAS_WIDTH - 2 - 7
    list_of_x_values = [7]
    width_used = 0
    x = 7
    y = 7
    width_remaining = canvas_frame_width - width_used
    width_of_rectangle_extreme = 100 + canvas_frame_width // NUM_COLUMNS
    while width_remaining != width_used:
        width_of_rectangle = random.randrange(20, width_of_rectangle_extreme)
        x += width_of_rectangle
        list_of_x_values.append(x)
        width_used += width_of_rectangle
        width_remaining = canvas_frame_width - width_used
        if width_remaining < width_of_rectangle_extreme:
            if width_remaining > 50:
                width_of_rectangle_extreme -= random.randrange(20, width_remaining - 21)
            else:
                x += width_remaining
                list_of_x_values.append(x)
        if width_remaining < width_of_rectangle_extreme:
            x += width_remaining
            list_of_x_values.append(x)
            break
    good_end_test(list_of_x_values)
    return list_of_x_values


# creates a list of the y coordinates for the initial grid of rectangles -- basically redundant :-O
def create_list_of_random_heights():
    canvas_frame_width = CANVAS_WIDTH - 2 - 7
    # 7 as starting number is to offset off frame
    list_of_y_values = [7]
    width_used = 0
    x = 7
    y = 7
    width_remaining = canvas_frame_width - width_used
    width_of_rectangle_extreme = 100 + canvas_frame_width // NUM_COLUMNS
    while width_remaining != width_used:
        width_of_rectangle = random.randrange(20, width_of_rectangle_extreme)
        x += width_of_rectangle
        list_of_y_values.append(x)
        width_used += width_of_rectangle
        width_remaining = canvas_frame_width - width_used
        if width_remaining < width_of_rectangle_extreme:
            if width_remaining > 50:
                width_of_rectangle_extreme -= random.randrange(20, width_remaining - 21)
            else:
                x += width_remaining
                list_of_y_values.append(x)
        if width_remaining < width_of_rectangle_extreme:
            x += width_remaining
            list_of_y_values.append(x)
            break
    good_end_test(list_of_y_values)
    return list_of_y_values


# ensures there isn't an extra box off the screen by making sure the last coordinate
# is the edge of the workable canvas
def good_end_test(alist):
    length = len(alist)
    if alist[length - 2] == 498:
        alist.pop()
    return alist


# makes the program appear full screen to ensure the screenshot captures the art itself
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


def make_canvas(width, height, title=None):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    objects = {}
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    app = FullScreenApp(top)
    # top.mainloop()
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()

    # canvas.bind("<Motion>", mouse_moved)
    return canvas


if __name__ == '__main__':
    main()
