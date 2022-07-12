import picounicorn
from random import randint
import random
import time

picounicorn.init()

w = picounicorn.get_width()
h = picounicorn.get_height()

# Initial probability of a grid square having a tree
initial_life = 0.25

# p = probability of life growing, f = probability of fire
p = 0.0001
f = 0.0005

# Each square's neighbour coordinates
hood = ((-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1))



# colors here instead of a lib/module
Black = [0,0,0]
White = [255,255,255]
Red = [255,0,0]
Lime = [0,255,0]
Blue = [0,0,255]
Yellow = [255,255,0]
Cyan = [0,255,255]
Magenta = [255,0,255]
Silver = [192,192,192]
Gray = [128,128,128]
Maroon = [128,0,0]
Olive = [128,128,0]
Green = [0,128,0]
Purple = [128,0,128]
Teal = [0,128,128]
Navy = [0,0,128]


colors = ( Black,White,Red,Lime,Blue,Yellow,Cyan,Magenta,Silver,Gray,Maroon,Olive,Green,Purple,Teal,Navy)

#while not picounicorn.is_pressed(picounicorn.BUTTON_A):  # Wait for Button A to be pressed
#    pass


# Function to populate the initial grid
def initialise():
    global life
    global space
    global new_life
    global new_space
    new_life = None
    new_space = None
    life = random.choice(colors)
    space = random.choice(colors)
    grid = {(x, y): (life if random.random() <= initial_life else space) for x in range(w) for y in range(h)}
    return grid

# Display the grid, in its current state, on UnicornHATMini
def show_grid(grid):
#    picounicorn.clear()
    for x in range(w):
        for y in range(h):
            picounicorn.set_pixel(x, y, *grid[(x, y)])
    
    
    # Go through grid, update grid squares based on state of
# square and neighbouring squares
def update_grid(grid):
    global new_space
    global new_life
    global space
    global life
    new_grid = {}
    for x in range(w):
        for y in range(h):
            count = 0
            for dx, dy in hood:
                if grid.get((x + dx, y + dy), space) == life:
                    count += 1
            #print(x,y,count)

            # if new colors are asked
            if not new_space:
                new_space = space
            if not new_life:
                new_life = life
            if grid[(x,y)] == life:
                if count < 2:
                    new_grid[(x,y)] = new_space
                elif count > 4:
                    new_grid[(x,y)] = new_space
                else:
                    new_grid[(x,y)] = new_life
            if grid[(x,y)] == space:
                if count == 3:
                    new_grid[(x,y)] = new_life
                else:
                    new_grid[(x,y)] = new_space
		

    #print (new_grid)
    space = new_space
    life = new_life
    new_space = None
    new_life = None

    return new_grid


# Main function. Initialises grid, then shows, updates, and
# waits for 1/60 of a second.
def main():
    global space
    global life
    global new_space
    global new_life

    global cnt_dupe
    global cnt_color
    global cnt_button
    global cnt_limit
    cnt_dupe = 0
    cnt_color = 0
    cnt_button = 0
    cnt_limit = 0
    grid = initialise()
    cycles = 0
    while True:
        # duplicate color detection
        if (space == life):
            grid = initialise()
            cycles = 0
            print("same colors!")
            cnt_dupe += 1
        # show the grid and update
        show_grid(grid)
        new_grid = update_grid(grid)
        # trying to change colors
        if (picounicorn.is_pressed(picounicorn.BUTTON_Y)):
            print("life color change")
            new_life = random.choice(colors)
        if (picounicorn.is_pressed(picounicorn.BUTTON_X)):
            print("space color change")
            new_space = random.choice(colors)
        if (picounicorn.is_pressed(picounicorn.BUTTON_B)):
            print("green on black")
            new_space = Black
            new_life = Green
        # duplicate grid detection
        if (new_grid == grid):
            grid = initialise()
            cycles = 0
            print("duplicate grid!")
            cnt_dupe += 1
        else:
            grid = new_grid
            cycles += 1
        # cycle limits
        if (cycles > 500):
            print("limit reached")
            cnt_limit += 1
            cycles = 0
            grid = initialise()
        # reset button
        if (picounicorn.is_pressed(picounicorn.BUTTON_A)):
            print("reset button (o)")
            cnt_button += 1
            cycles = 0
            grid = initialise()
        # update interval
        time.sleep(1 / 8.0)


# Catches control-c and exits cleanly
try:
    main()

except KeyboardInterrupt:
    print("Stats:")
    print("Max cycles:%d" % cnt_limit)
    print("Button press:%d" % cnt_button)
    print("Duplicates:%d" % cnt_dupe)
    print("Same Colors:%d" % cnt_color)
    print("Exiting")


