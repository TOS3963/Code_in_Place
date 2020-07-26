import random
import time
import tkinter
import random

SQSIZE = 20
N_ROWS = 24
N_COL = 10
CANVAS_WIDTH = SQSIZE * N_COL
CANVAS_HEIGHT = SQSIZE * N_ROWS
# Any positive integer > 0 and lower than 50
# Larger = Slower
SPEED = 10


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'TETRIS')
    flag = True
    name = choice()
    rotation = 0
    active_list = get_tetraminos(canvas, name)
    canvas.bind('<Key>', lambda keypress: controls(keypress, canvas, active_list))
    canvas.focus_set()
    canvas.update()
    game_over = False
    render_count = 0
    while not game_over:
        # Define Major Flow
        render_count = action_phase(canvas, active_list, render_count)
        delete_row(canvas)
        game_over = check_game_over(canvas)
        name = choice()
        active_list = get_tetraminos(canvas, name)
    canvas.unbind('<Key>', lambda keypress: controls(keypress, canvas, active_list))
    print("GAMEOVER")
    canvas.mainloop()

def check_and_move_blocks(canvas, active_list, shift_list):

    valid1 = is_block_move_valid(canvas, active_list[0], active_list, shift_list[0], shift_list[1])
    valid2 = is_block_move_valid(canvas, active_list[1], active_list, shift_list[2], shift_list[3])
    valid3 = is_block_move_valid(canvas, active_list[2], active_list, shift_list[4], shift_list[5])
    valid4 = is_block_move_valid(canvas, active_list[3], active_list, shift_list[6], shift_list[7])

    if valid1 and valid2 and valid3 and valid4:
        canvas.move(b1, SQSIZE * shift_list[0], SQSIZE * shift_list[1])
        canvas.move(b2, SQSIZE * shift_list[2], SQSIZE * shift_list[3])
        canvas.move(b3, SQSIZE * shift_list[4], SQSIZE * shift_list[5])
        canvas.move(b4, SQSIZE * shift_list[6], SQSIZE * shift_list[7])

def rotate(canvas, active_list, name, rotation):

    if name == 'Line Piece':
        #Mark: this shift to most wide column shift
        if rotation == 0 or 2:

            shift_list = [-1, -1, 0, 0, 1, 1, 2, 2]
            check_and_move_blocks(canvas, block, active_list, shift_list)

        elif rotation == 1 or 3:

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
            shift_list = [0,0,0,0,1,1,-1,1]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 1:
            shift_list = [0,0,-1,-1,-2,-2,1,-1]
            check_and_move_blocks(canvas, active_list, shift_list)
        if rotation == 2:
            shift_list = [1,0,-1,0,0,1,0,1]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 3:
            shift_list = [-1,0,2,-1,1,0,0,-1]
            check_and_move_blocks(canvas, active_list, shift_list)

    elif name == 'Squiggly':
        if rotation == 0 or 2:
            shift_list = [1,1,0,0,-1,1,-1,-1]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 1 or 3:
            shift_list = [-1,-1,0,0,1,-1,1,1]
            check_and_move_blocks(canvas, active_list, shift_list)

    elif name == 'Reverse Squiggly':
        if rotation == 0 or 2:
            shift_list = [0,1,-1,0,2,1,1,0]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 1 or 3:
            shift_list = [0,-1,1,0,-2,-1,-1,0]
            check_and_move_blocks(canvas, active_list, shift_list)

    elif name == 'Square':
        #Left this choice in as representation
        #Rotating square does nothing
        pass

    elif name == 'T-Block':
        if rotation == 0:
            shift_list = [1,1,0,0,0,0,0,0]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 1:
            shift_list = [0,0,-1,0,-1,0,1,1]
            check_and_move_blocks(canvas, active_list, shift_list)
        if rotation == 2:
            shift_list = [0,0,0,0,0,0,-1,-1]
            check_and_move_blocks(canvas, active_list, shift_list)
        elif rotation == 3:
            shift_list = [-1,-1,1,1,1,1,0,0]
            check_and_move_blocks(canvas, active_list, shift_list)

    if rotation < 3:
        rotation += 1
    else:
        rotation = 0
    return rotation

def out_of_bounds(new):
    c1 = new[0] =< -1
    c2 = new[2] >= CANVAS_WIDTH + 1
    c3 = new[3] >= CANVAS_HEIGHT
    if c1 or c2 or c3:
        return True

def is_block_move_valid(canvas, block, active_list, xshift, yshift):
    current = canvas.coords(block)
    #Reduces scope of box by 1 pixel border
    #and then shifts cell according to potential movement
    x1 = current[0] + 1 + (SQSIZE * xshift)
    y1 = current[1] + 1 + (SQSIZE * yshift)
    x2 = current[2] - 1 + (SQSIZE * xshift)
    y2 = current[3] - 1 + (SQSIZE * xshift)
    new = [x1, y1, x2, y2]
    next = canvas.find_overlapping(x1, y1, x2, y2)
    #THIS IF STATEMENT CHECKS IF ITS OVERLAPPING
    #ANYTHING AT ALL
    #TODO: ADD BOUNDARY FUNCTION/ALL OTHER OUT OF BOUNDS WILL BE IRRELEVANT
    if len(next) > 0:
        #THIS FOR LOOP CHECKS IF WHAT IT'S OVERLAPPING IS
        #An ACTIVE BLOCK
        for item in active_list:
            a = canvas.coords(item)
            a1 = a[0] + 1
            b1 = a[1] + 1
            a2 = a[2] - 1
            b2 = a[3] - 1
            temp = [a1, b1, a2, b2]
            if new == temp:
                #OVERLAPPING A BLOCK IN ACTIVE PIECE
                #SO THIS MOVE IS VALID
                return True
        #SINCE ITS OVERLAPPING AND NOT IN ACTIVE LIST
        #THIS MOVE ISN'T VALID
        else:
            return False
    #THIS MOVE IS VALID
    else:
        return True


def check_game_over(canvas):
    x1 = -1
    y1 = -SQSIZE - 1
    x2 = CANVAS_WIDTH - 1
    y2 = -1
    check_row = canvas.find_overlapping(x1, y1, x2, y2)
    if len(check_row) >= N_COL:
        return True


def choice():
    num = random.randint(1, 7)
    names = {1: "Line Piece", 2: 'L-Block', 3: 'Reverse L-Block', 4: 'Squiggly', 5: 'Reverse Squiggly', 6: 'Square',
             7: 'T-Block'}
    name = names[num]
    return name


def get_tetraminos(canvas, name):
    colors = ["red", "orange", "yellow", "green", "blue", "violet", 'cyan']

    choice = name
    if choice == 'Line Piece':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, 0, -SQSIZE)
        b3 = set_square(canvas)
        canvas.move(b3, 0, -SQSIZE * 2)
        b4 = set_square(canvas)
        canvas.move(b4, 0, -SQSIZE * 3)
        colorchoice = colors[0]

    elif choice == 'L-Block':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, 0, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, 0, -SQSIZE * 2)
        colorchoice = colors[1]

    elif choice == 'Reverse L-Block':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, SQSIZE, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE, -SQSIZE * 2)
        colorchoice = colors[2]

    elif choice == 'Squiggly':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, SQSIZE, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE * 2, -SQSIZE)
        colorchoice = colors[3]

    elif choice == 'Reverse Squiggly':
        b1 = set_square(canvas)
        canvas.move(b1, SQSIZE, 0)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE * 2, 0)
        b3 = set_square(canvas)
        canvas.move(b3, 0, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE, -SQSIZE)
        colorchoice = colors[4]

    elif choice == 'Square':
        b1 = set_square(canvas)
        b2 = set_square(canvas)
        canvas.move(b2, SQSIZE, 0)
        b3 = set_square(canvas)
        canvas.move(b3, 0, -SQSIZE)
        b4 = set_square(canvas)
        canvas.move(b4, SQSIZE, -SQSIZE)
        colorchoice = colors[5]

    elif choice == 'T-Block':
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
        canvas.itemconfig(item, fill= colorchoice)
    return tetramino


def render(canvas, render_count):
    time.sleep(1 / 100)
    canvas.update()
    render_count += 1
    return render_count


def action_phase(canvas, active_list, render_count):
    flag = not_blocked(canvas, active_list)
    while flag:
        #TODO: THIS WORKS,BUT GRAVITY DOESNT NEED TO PASS OUT RENDER COUNT
        render_count = gravity(canvas, active_list, render_count)
        render_count = render(canvas, render_count)
        flag = not_blocked(canvas, active_list)
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


def check_row(canvas, active_block):
    row = get_top_y(canvas, active_block) // SQSIZE
    x = int(row)
    return str(x)


def add_piece(canvas):
    new = set_square(canvas)
    canvas.update()
    return new

#TODO: THIS FUNCTION WILL BE IRRELAVENT THANKS TO CHECKANDMOVE ONCE BOUNDARY IS ADDED
#TODO: DOUBLE CHECK THAT ALL FUNCTIONS PASS BEFORE DELETE/EDIT
def not_blocked(canvas, active_list):
    flag = True
    if not_hit_floor(canvas, active_list):
        lowest_y = get_block_lowest_y(canvas, active_list)
        for item in active_list:
            item_bottom_y = get_bottom_y(canvas, item)
            if item_bottom_y == lowest_y:
                if not square_available(canvas, item):
                    flag = False
            #elif check if edge is exposed
            # check if item_bottom_y + x1 overlaps
                #if not then check if square not available
        return flag
#TODO: SAME AS ABOVE
def get_block_lowest_y(canvas, active_list):
    lowest = 0
    for item in active_list:
        piece_bottom_y = get_bottom_y(canvas, item)
        if piece_bottom_y > lowest:
            lowest = piece_bottom_y
    return lowest

#TODO: SAME AS ABOVE
def right_available(canvas, active_list):
    measure = 0
    for item in active_list:
        right = get_right_x(canvas, item)
        if right > measure:
            rightmost = item
            measure = right
    current = canvas.coords(rightmost)
    x1 = current[0] + SQSIZE + 1
    y1 = current[1] + 1
    x2 = current[2] + SQSIZE - 1
    y2 = current[3] - 1
    next = canvas.find_overlapping(x1, y1, x2, y2)
    if len(next) > 0 or x2 >= CANVAS_WIDTH:
        return False
    else:
        return True

#TODO: SAME AS ABOVE
def left_available(canvas, active_list):
    measure = CANVAS_WIDTH
    for item in active_list:
        left = get_left_x(canvas, item)
        if left < measure:
            leftmost = item
            measure = left

    current = canvas.coords(leftmost)
    x1 = current[0] - SQSIZE + 1
    y1 = current[1] + 1
    x2 = current[2] - SQSIZE - 1
    y2 = current[3] - 1
    next = canvas.find_overlapping(x1, y1, x2, y2)
    if len(next) > 0 or x1 <= 0:
        return False
    else:
        return True

#TODO: SAME AS ABOVE
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

#TODO: RENAME RENDER COUNT TO GRAVITY COUNT
def gravity(canvas, active_list, render_count):
    if render_count == SPEED:
        for item in active_list:
            canvas.move(item, 0, SQSIZE)
        render_count = 0
    return render_count


def set_square(canvas):
    start_x = (N_COL - 1) // 2 * SQSIZE
    end_x = start_x + SQSIZE
    piece = canvas.create_rectangle(start_x, -SQSIZE, end_x, 0, tags='Block')
    return piece

#TODO: IF CHECK AND MOVE WORKS PROPERLY EDIT MOVE FUNCTIONALITY
#TODO: add a shift_lift of all the same number and pass through check and move
def controls(keypress, canvas, active_list, name, rotation):
    comm = keypress.keysym
    x = 0
    y = 0
    flag = True
    if comm == 'Left' and left_available(canvas, active_list):
        x = -SQSIZE
    elif comm == 'Right' and right_available(canvas, active_list):
        x = SQSIZE
    elif comm == 'Down' and not_hit_floor(canvas, active_list):
        y = SQSIZE
    elif comm == 'Up':
        rotate(canvas, active_list, name, rotation)
    else:
        flag = False
    if flag:
        for item in active_list:
            canvas.move(item, x, y)
            canvas.update()

#TODO: THIS FUNCTION IS IRRELEVANT THANKS TO CHECK AND MOVE
#TODO: DOUBLE CHECK EVERYTHING WORKS BEFORE DELETING
def not_hit_floor(canvas, active_list):
    for item in active_list:
        piece_bottom_y = get_bottom_y(canvas, item)
        if piece_bottom_y >= CANVAS_HEIGHT:
            return False
    else:
        return True


'''These functions get the coordinates of any singular block'''


def get_left_x(canvas, object):
    return canvas.coords(object)[0]


def get_top_y(canvas, object):
    return canvas.coords(object)[1]


def get_bottom_y(canvas, object):
    return canvas.coords(object)[3]


def get_right_x(canvas, object):
    return canvas.coords(object)[2]


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
