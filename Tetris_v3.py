import time
import tkinter
import random

SQSIZE = 40
N_ROWS = 16
N_COL = 10
CANVAS_WIDTH = SQSIZE * N_COL
CANVAS_HEIGHT = SQSIZE * N_ROWS
# Any positive integer > 0 and lower than 50
# Larger = Slower
SPEED = 35


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'TETRIS')
    name = choice()
    active_list = get_tetraminos(canvas, name)
    canvas.bind('<Key>', lambda keypress: controls(keypress, canvas, active_list, name))
    canvas.focus_set()
    canvas.update()
    game_over = False
    render_count = 0
    score = 0
    while not game_over:
        # Define Major Flow
        render_count = action_phase(canvas, active_list, render_count)
        score += delete_row(canvas)
        game_over = check_game_over(canvas)
        name = choice()
        active_list = get_tetraminos(canvas, name)
    print(score)
    print("GameOver")
    canvas.unbind('<Key>')
    canvas.mainloop()


# THERE IS A BETTER WAY TO WRITE THIS
# SHIFT LIST AS NESTED LIST
def check_and_move_blocks(canvas, active_list, shift_list):
    # I could streamline this by using tuples in my shift list
    # However this works for now
    valid1 = is_block_move_valid(canvas, active_list[0], active_list, shift_list[0], shift_list[1])
    valid2 = is_block_move_valid(canvas, active_list[1], active_list, shift_list[2], shift_list[3])
    valid3 = is_block_move_valid(canvas, active_list[2], active_list, shift_list[4], shift_list[5])
    valid4 = is_block_move_valid(canvas, active_list[3], active_list, shift_list[6], shift_list[7])

    if valid1 and valid2 and valid3 and valid4:
        canvas.move(active_list[0], SQSIZE * shift_list[0], SQSIZE * shift_list[1])
        canvas.move(active_list[1], SQSIZE * shift_list[2], SQSIZE * shift_list[3])
        canvas.move(active_list[2], SQSIZE * shift_list[4], SQSIZE * shift_list[5])
        canvas.move(active_list[3], SQSIZE * shift_list[6], SQSIZE * shift_list[7])
        return True
    else:
        return False


def rotate(canvas, active_list, name):
    #THIS FUNCTION REARRANGES THE BLOCKS FOR
    #PERCIEVED ROTATION. HOWEVER THE BLOCKS STAY
    #IN ORDER FROM LEFT TO RIGHT, BOTTOM TO TOP
    reference_block = active_list[0]

    rotation = int(canvas.gettags(reference_block)[0])

    if name == 'Line Piece':
        # Mark: this shift to most wide column shift
        if rotation == 0 or rotation == 2:

            shift_list = [-1, -1, 0, 0, 1, 1, 2, 2]
            check_and_move_blocks(canvas, active_list, shift_list)

        elif rotation == 1 or rotation == 3:

            shift_list = [1, 1, 0, 0, -1, -1, -2, -2]
            check_and_move_blocks(canvas, active_list, shift_list)

    elif name == 'L-Block':
        if rotation == 0:

            shift_list = [0, 0, -1, -1, 1, 0, 2, 1]
            check_and_move_blocks(canvas, active_list, shift_list)

        elif rotation == 1:

            shift_list = [1, 0, 1, 0, -1, -1, -1, -1]
            check_and_move_blocks(canvas, active_list, shift_list)

        if rotation == 2:

            shift_list = [-2, 0, -1, 1, 1, 2, 0, 1]
            check_and_move_blocks(canvas, active_list, shift_list)

        elif rotation == 3:
            shift_list = [1, 0, 1, 0, -1, -1, -1, -1]
            check_and_move_blocks(canvas, active_list, shift_list)

    elif name == 'Reverse L-Block':
        if rotation == 0:
            shift_list = [0, 0, 0, 0, 1, 1, -1, 1]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 1:
            shift_list = [0, 0, -1, -1, -2, -2, 1, -1]
            check_and_move_blocks(canvas, active_list, shift_list)
        if rotation == 2:
            shift_list = [1, 0, -1, 0, 0, 1, 0, 1]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 3:
            shift_list = [-1, 0, 2, 1, 1, 0, 0, -1]
            check_and_move_blocks(canvas, active_list, shift_list)

    elif name == 'Squiggly':
        if rotation == 0 or rotation == 2:
            shift_list = [2, 0, 1, -1, 0, 0, -1, -1]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 1 or 3:
            shift_list = [-2, 0, -1, 1, 0, 0, 1, 1]
            check_and_move_blocks(canvas, active_list, shift_list)

    elif name == 'Reverse Squiggly':
        if rotation == 0 or rotation == 2:
            shift_list = [0, 1, -1, 0, 2, 1, 1, 0]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 1 or rotation == 3:
            shift_list = [0, -1, 1, 0, -2, -1, -1, 0]
            check_and_move_blocks(canvas, active_list, shift_list)

    elif name == 'Square':
        # Left this in as representation
        # Rotating square does nothing
        pass

    elif name == 'T-Block':
        if rotation == 0:
            shift_list = [1, 1, 0, 0, 0, 0, 0, 0]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 1:
            shift_list = [0, 0, -1, 0, -1, 0, 1, 1]
            check_and_move_blocks(canvas, active_list, shift_list)
        if rotation == 2:
            shift_list = [0, 0, 0, 0, 0, 0, -1, -1]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 3:
            shift_list = [-1, -1, 1, 0, 1, 0, 0, 0]
            check_and_move_blocks(canvas, active_list, shift_list)
    if rotation < 3:
        rotation += 1
    elif rotation == 3:
        rotation = 0
    rotation = str(rotation)
    canvas.itemconfig(reference_block, tags=rotation)


def out_of_bounds(new):
    # Left Border Check
    c1 = new[0] <= -1
    # Right Border Check
    c2 = new[2] >= CANVAS_WIDTH + 1
    # Floor Check
    c3 = new[3] >= CANVAS_HEIGHT + 1
    if c1 or c2 or c3:
        return True
    else:
        return False


def is_block_move_valid(canvas, block, active_list, xshift, yshift):
    current = canvas.coords(block)
    # Reduces scope of box by 1 pixel border
    # and then shifts cell according to potential movement
    # Prevents accidental overlap of borders
    x1 = current[0] + 1 + (SQSIZE * xshift)
    y1 = current[1] + 1 + (SQSIZE * yshift)
    x2 = current[2] - 1 + (SQSIZE * xshift)
    y2 = current[3] - 1 + (SQSIZE * yshift)
    #sets new coordinates to list
    new = [x1, y1, x2, y2]
    #Collects values of of anticipated move overlaps
    next = canvas.find_overlapping(x1, y1, x2, y2)

    # TIME FOR LOGIC!
    # First Checks if move is out of bounds
    if out_of_bounds(new) == True:
        return False
    else:
        # THIS IF STATEMENT CHECKS IF ITS OVERLAPPING
        # ANYTHING AT ALL
        if len(next) > 0:
            # THIS FOR LOOP CHECKS IF WHAT IT'S OVERLAPPING IS
            # A piece of the active block
            for item in active_list:
                a = canvas.coords(item)
                a1 = a[0] + 1
                b1 = a[1] + 1
                a2 = a[2] - 1
                b2 = a[3] - 1
                temp = [a1, b1, a2, b2]
                if new == temp:
                    # OVERLAPPING A BLOCK IN ACTIVE PIECE
                    # SO THIS MOVE IS VALID SINCE MOVE WILL BE AVAILABLE
                    return True
            # SINCE ITS OVERLAPPING AND NOT IN ACTIVE LIST
            # THIS MOVE ISN'T VALID
            else:
                return False
        # NOT OVERLAPPING ANYTHING
        # SO THIS MOVE IS VALID
        else:
            return True


def check_game_over(canvas):
    x1 = -1
    y1 = -SQSIZE - 1
    x2 = CANVAS_WIDTH - 1
    y2 = -1
    check_row = canvas.find_overlapping(x1, y1, x2, y2)
    if len(check_row) > 0:
        return True


def choice():
    num = random.randint(1, 7)
    names = {1: "Line Piece", 2: 'L-Block', 3: 'Reverse L-Block', 4: 'Squiggly', 5: 'Reverse Squiggly', 6: 'Square',
             7: 'T-Block'}
    name = names[num]
    return name


def get_tetraminos(canvas, name):
    colors = ["red", "orange", "yellow", "green", "blue", "violet", 'cyan']

    if name == 'Line Piece':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, 0, -SQSIZE)
        b3 = set_square(canvas)
        canvas.move(b3, 0, -SQSIZE * 2)
        b4 = set_square(canvas)
        canvas.move(b4, 0, -SQSIZE * 3)
        colorchoice = colors[0]

    elif name == 'L-Block':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, 0, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, 0, -SQSIZE * 2)
        colorchoice = colors[1]

    elif name == 'Reverse L-Block':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, SQSIZE, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE, -SQSIZE * 2)
        colorchoice = colors[2]

    elif name == 'Squiggly':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, SQSIZE, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE * 2, -SQSIZE)
        colorchoice = colors[3]

    elif name == 'Reverse Squiggly':
        b1 = set_square(canvas)
        canvas.move(b1, SQSIZE, 0)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE * 2, 0)
        b3 = set_square(canvas)
        canvas.move(b3, 0, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE, -SQSIZE)
        colorchoice = colors[4]

    elif name == 'Square':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, 0, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE, -SQSIZE)
        colorchoice = colors[5]

    elif name == 'T-Block':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, SQSIZE * 2, 0)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE, -SQSIZE)
        colorchoice = colors[6]

    tetramino = [b1, b2, b3, b4]
    for item in tetramino:
        canvas.itemconfig(item, fill=colorchoice)
    return tetramino


def render(canvas, render_count):
    time.sleep(1 / 100)
    canvas.update()
    render_count += 1
    return render_count


def action_phase(canvas, active_list, render_count):
    flag = True  # not_blocked(canvas, active_list)
    while flag:
        flag = gravity(canvas, active_list, render_count)
        render_count = render(canvas, render_count)
    return render_count


def delete_row(canvas):
    score = 0
    for n in range(N_ROWS):
        x1 = -1
        y1 = n * SQSIZE - 1
        x2 = CANVAS_WIDTH + 1
        y2 = (n + 1) * SQSIZE + 1
        check_row = canvas.find_enclosed(x1, y1, x2, y2)
        if len(check_row) >= N_COL:
            for item in check_row:
                canvas.delete(item)
                score += 1
            a2 = x2
            b2 = y1 + 2
            above = canvas.find_enclosed(-1, -1, a2, b2)
            for item in above:
                canvas.move(item, 0, SQSIZE)
    score /= N_COL
    actualscore = score_calc(score)
    return actualscore


def score_calc(score):
    actualscore = 0
    if score == 1:
        actualscore = 100
    if score == 2:
        actualscore = 300
    if score == 3:
        actualscore = 700
    if score == 4:
        actualscore = 1500
    # print(actualscore)
    return actualscore

def gravity(canvas, active_list, render_count):
    flag = True
    if render_count % SPEED == 0:
        flag = check_and_move_blocks(canvas, active_list, shift_list=[0, 1, 0, 1, 0, 1, 0, 1])
    return flag


def set_square(canvas):
    start_x = (N_COL - 1) // 2 * SQSIZE
    end_x = start_x + SQSIZE
    piece = canvas.create_rectangle(start_x, -SQSIZE, end_x, 0, tags='0')
    return piece


def controls(keypress, canvas, active_list, name):
    comm = keypress.keysym
    x = 0
    y = 0
    flag = True
    if comm == 'Left':
        shift_list = [-1, 0, -1, 0, -1, 0, -1, 0]
        check_and_move_blocks(canvas, active_list, shift_list)
    elif comm == 'Right':
        shift_list = [1, 0, 1, 0, 1, 0, 1, 0]
        check_and_move_blocks(canvas, active_list, shift_list)
    elif comm == 'Down':
        shift_list = [0, 1, 0, 1, 0, 1, 0, 1]
        check_and_move_blocks(canvas, active_list, shift_list)
    elif comm == 'Up':
        rotate(canvas, active_list, name)
    else:
        flag = False
    if flag:
        for item in active_list:
            canvas.move(item, x, y)
            canvas.update()


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
