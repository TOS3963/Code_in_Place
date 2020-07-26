import random
import time
import tkinter
import random

SQSIZE = 20
N_ROWS = 6
N_COL = 10
CANVAS_WIDTH = SQSIZE * N_COL
CANVAS_HEIGHT = SQSIZE * N_ROWS
# Any positive integer > 0 and lower than 50
# Larger = Slower
SPEED = 20


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'TETRIS')
    flag = True
    active_block = add_piece(canvas)
    canvas.bind('<Key>', lambda keypress: controls(keypress, canvas, active_block))
    canvas.focus_set()
    canvas.update()
    game_over = False
    render_count = 0
    while not game_over:
        # Define Major Flow

        render_count = action_phase(canvas, active_block, render_count)
        active_block = add_piece(canvas)
        # anchors the piece to last location
        # Tags the line where the piece has stopped
        # Delete
        # Checks if any row can be deleted
        # Does the count of objects with line tag = N_COLS


'''
def get_tetraminos(canvas):
    choice = random.randomint(1,7)
    if choice == 1:
        #SQUARE
        b1 = set_square(canvas)
        canvas.move(b1, SQSIZE, 0)
        b2 = set_square(canvas)
        canvas.move(b2, 0, -SQSIZE)
        b3 = set_square(canvas)
        canvas.move(b3, -SQSIZE, SQSIZE)
        b4
    elif choice == 2
        squiggly
    reverse_squiggly
    line_piece
    l_block
    reverse_l_block
    t_block
'''


def render(canvas, render_count):
    time.sleep(1 / 50)
    canvas.update()
    render_count += 1
    return render_count


def action_phase(canvas, active_block, render_count):
    flag = not_blocked(canvas, active_block)
    while flag:
        render_count = gravity(canvas, active_block, render_count)
        render_count = render(canvas, render_count)
        flag = not_blocked(canvas, active_block)
    delete_row(canvas)
    return render_count


def delete_row(canvas):
    for n in range(N_ROWS):
        x1 = -1
        y1 = n * SQSIZE - 1
        x2 = CANVAS_WIDTH + 1
        y2 = (n + 1) * SQSIZE + 1
        check_row = canvas.find_enclosed(x1, y1, x2, y2)
        if len(check_row) >= N_COL:
            for item in check_row:
                canvas.delete(item)
            a2 = x2
            b2 = y1 + 2
            above = canvas.find_enclosed(-1, -1, a2, b2)
            for item in above:
                canvas.move(item, 0, SQSIZE)


'''
def delete_row(canvas):
    for n in range(N_ROWS):
        row = "Row" + str(n)
        rowlist = canvas.find_withtag(row)
        if len(rowlist) >= N_COL:
            canvas.delete(row)
'''
# This function will remove the active player piece status
# and anchor the piece to its row position
'''
def set_piece(canvas, active_block):
    row = "Row" + str(check_row(canvas, active_block))
    canvas.addtag_withtag(row, active_block)
'''


# Write code to change tag for row position
def check_row(canvas, active_block):
    row = get_top_y(canvas, active_block) // SQSIZE
    x = int(row)
    return str(x)


def add_piece(canvas):
    new = set_square(canvas)
    canvas.update()
    return new


def not_blocked(canvas, active_block):
    if not_hit_floor(canvas, active_block) and square_available(canvas, active_block):
        return True
    else:
        return False


def right_available(canvas, active_block):
    current = canvas.coords(active_block)
    x1 = current[0] + SQSIZE + 1
    y1 = current[1] + 1
    x2 = current[2] + SQSIZE - 1
    y2 = current[3] - 1
    item_below = canvas.find_overlapping(x1, y1, x2, y2)
    if len(item_below) > 0:
        return False
    else:
        return True


def left_available(canvas, active_block):
    current = canvas.coords(active_block)
    x1 = current[0] - SQSIZE + 1
    y1 = current[1] + 1
    x2 = current[2] - SQSIZE - 1
    y2 = current[3] - 1
    item_below = canvas.find_overlapping(x1, y1, x2, y2)
    if len(item_below) > 0:
        return False
    else:
        return True


def square_available(canvas, active_block):
    current = canvas.coords(active_block)
    x1 = current[0] + 1
    y1 = current[1] + SQSIZE + 1
    x2 = current[2] - 1
    y2 = current[3] + SQSIZE - 1
    item_below = canvas.find_overlapping(x1, y1, x2, y2)
    if len(item_below) > 0:
        return False
    else:
        return True


def gravity(canvas, piece, render_count):
    if render_count == SPEED:
        canvas.move(piece, 0, SQSIZE)
        render_count = 0
    return render_count
    # move active pieces down certain amount of time


def set_square(canvas):
    start_x = (N_COL - 1) // 2 * SQSIZE
    end_x = start_x + SQSIZE
    piece = canvas.create_rectangle(start_x, -SQSIZE, end_x, 0, fill='black', tags='Block')
    return piece


def controls(keypress, canvas, piece):
    comm = keypress.keysym
    x = 0
    y = 0
    if comm == 'Left' and left_available(canvas, piece) and get_left_x(canvas, piece) >= SQSIZE:
        x = -SQSIZE
    if comm == 'Right' and right_available(canvas, piece) and get_left_x(canvas, piece) <= (CANVAS_WIDTH - SQSIZE * 2):
        x = SQSIZE
    if comm == 'Down' and not_hit_floor(canvas, piece):
        y = SQSIZE
    if comm == 'Up':
        print('Rotate')
    canvas.move(piece, x, y)
    canvas.update()


def not_hit_floor(canvas, piece):
    piece_bottom_y = get_top_y(canvas, piece) + SQSIZE
    return piece_bottom_y < CANVAS_HEIGHT


def get_left_x(canvas, object):
    return canvas.coords(object)[0]


def get_top_y(canvas, object):
    return canvas.coords(object)[1]


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
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    canvas.xview_scroll(8, 'units')  # add this so (0, 0) works correctly
    canvas.yview_scroll(8, 'units')  # otherwise it's clipped off

    return canvas


if __name__ == '__main__':
    main()
