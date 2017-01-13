'''
This Candy Crush example was made by Clara Lo, with improvements
by Wallace Mak and Gibson Lam.
'''

import turtle
import random

turtle.reset()

# Set up the window
turtle.setup(600, 460)
turtle.bgpic("candy_crush_bg.gif")

# Turn off the turtle animations
turtle.tracer(False)

# Variables storing the total numbers of candies in a row/column
# Candies are at coordinate (X, Y) where X is an integer in the range 0...6 and Y is an integer in the range 0...6
num_of_candies_in_row = 7
num_of_candies_in_col = 7

# Variable storing the size of the candies
candy_size = 60

# Variable storing the speed of the candy turtles
candy_speed = 7

# A list storing the file names of the candy images
candy_image = ["candy0.gif", "candy1.gif", "candy2.gif",
               "candy3.gif", "candy4.gif", "candy5.gif","candy6.gif"]

# Variable storing the total number of types of candies
num_of_candy_type = len(candy_image)

# Variable storing the special candy type value (-1), representing no candy at that location
nothing_in_cell = -1

# A 2D list storing the candy locations on the screen
candy_pos = [[(-110, -180), (-50, -180), (10, -180), (70, -180), (130, -180), (190, -180), (250, -180)],
             [(-110, -120), (-50, -120), (10, -120), (70, -120), (130, -120), (190, -120), (250, -120)],
             [(-110,  -60), (-50,  -60), (10,  -60), (70,  -60), (130,  -60), (190,  -60), (250,  -60)],
             [(-110,    0), (-50,    0), (10,    0), (70,    0), (130,    0), (190,    0), (250,    0)],
             [(-110,   60), (-50,   60), (10,   60), (70,   60), (130,   60), (190,   60), (250,   60)],
             [(-110,  120), (-50,  120), (10,  120), (70,  120), (130,  120), (190,  120), (250,  120)],
             [(-110,  180), (-50,  180), (10,  180), (70,  180), (130,  180), (190,  180), (250,  180)]]

# A 2D list storing the candy types at the corresponding locations in the play area
candy_map = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1]]

# A 2D list storing the "candies" turtles
# It will be initialized later and will have the same structure as candy_map
candies = []

# Variables storing the row number and column number of the firstly-clicked candy (for candy swapping)
firstly_clicked_candy_row = -1
firstly_clicked_candy_col = -1

# Variable indicating whether the firstly-clicked candy is clicked 
# If it is False, that means the user has yet to click on the first candy for swapping;
# If it is True, that means the user has already clicked on the first candy for swapping,
# so the next candy to be clicked is the second candy for swapping
first_candy_clicked = False

# Variable storing the minimum number of adjacent candies needed to form a matched group
minimum_num_of_candies_required_for_matching = 3

# Variables storing the matched candies locations which is detected by the find_any_matched_group function
matched_group = []

# Variable indicating whether the game is over
end = False

# Variable used by turtle.ontimer() for some delay between two executions of the handle_matched_candies function
delay = 250

# Variable storing the player's score
score = 0

# Turtle showing the player's score
score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.up()
score_turtle.goto(-220, -170)
score_turtle.pencolor("gray20")

# Variable storing the time left (in seconds)
time_left = 60

# Turtle showing the time left
time_turtle = turtle.Turtle()
time_turtle.hideturtle()
time_turtle.up()
time_turtle.pencolor("gray20")
time_turtle.goto(-220, -65)

# Add shapes from the gif image files
for i in range(num_of_candy_type):
    turtle.addshape(candy_image[i])

def generate_candies_turtles():

    # This function uses a for-loop to generate a list of lists of turtles 
    # with the same structure as candy_map to represent all the candies

    global candies

    for row in range(num_of_candies_in_row):

        # Create an empty list for storing the candy turtles
        candy_list = []

        for col in range(num_of_candies_in_col):

            # Create one turtle for one candy
            one_candy = turtle.Turtle()

            # Make the turtle move in a different speed
            one_candy.speed(candy_speed)

            # Move the turtle to the appropriate location and make it face down
            # (instead of the default east direction)
            one_candy.up()
            one_candy.right(90)
            one_candy.goto(candy_pos[row][col])

            # Append the turtle to the candy_list
            candy_list.append(one_candy)

        # Add candy_list, which is a list of 7 candy turtles, to another list
        # called candies to produce a list of lists of turtles (i.e. a 2D list)
        candies.append(candy_list)

def generate_candy_map():

    # This function generates the candy map by filling random numbers
    # (representing random candy types) into the candy_map 2D list
        
    global candy_map
    
    for row in range(num_of_candies_in_row):
        for col in range(num_of_candies_in_col):

            # Randomly generate an integer to represent a random candy type
            candy_map[row][col] = random.randrange(num_of_candy_type)

            # Regenerate the number until there is no matched group of candies
            # as the game should start with no matched group of candies
            while len(find_any_matched_group()) != 0:
                candy_map[row][col] = random.randrange(num_of_candy_type)

def countdown():

    # This function updates the "time left" display and make the game over when the time is up

    global time_left

    # Clear the previous "time left" display
    time_turtle.clear()
    time_turtle.write(str(round(time_left,1)), align="center", font=("Comic Sans MS", 16, "bold"))

    # If there is still some time left, schedule another execution of this function
    if time_left > 0:
        time_left -= 0.1
        turtle.ontimer(countdown, 100)

    # If the time is up, the game should be over, schedule the execution of game_over
    else:
        turtle.ontimer(game_over, 1000)

def candy(row, col):

    # This function returns the candy type at the location (row, col)
    # If (row, col) is out of range, nothing_in_cell is returned

    # If the numbers of row and column are out of range, return nothing_in_cell
    if row < 0 or row >= num_of_candies_in_row or col < 0 or col >= num_of_candies_in_col:
        return nothing_in_cell

    # If not, return the requested value
    else:
        return candy_map[row][col]

def swap_candies(first_candy_row, first_candy_col, second_candy_row, second_candy_col):

    # This function handles the swap candies animation between neighbouring candies

    # Save the locations
    first_candy_pos = candies[first_candy_row][first_candy_col].pos()
    second_candy_pos = candies[second_candy_row][second_candy_col].pos()

    turtle.tracer(True)
    # Move the first turtle
    candies[first_candy_row][first_candy_col].goto(second_candy_pos)
    # Move the second turtle
    candies[second_candy_row][second_candy_col].goto(first_candy_pos)
    turtle.tracer(False)

    # Move the turtles back to their original positions
    candies[first_candy_row][first_candy_col].goto(first_candy_pos)
    candies[second_candy_row][second_candy_col].goto(second_candy_pos)

def highlight_candy(row, col):

    # This function highlights the candy at (row, col) using a box

    global candies

    # Save the current position and heading of the candy
    pos = candies[row][col].pos()
    heading = candies[row][col].heading()

    # Draw a box around it
    candies[row][col].setpos(pos[0] - candy_size / 2, pos[1] + candy_size / 2)
    candies[row][col].down()
    for _ in range(4):
        candies[row][col].forward(candy_size)
        candies[row][col].left(90)
    candies[row][col].up()

    # Restore the position and heading of the candy
    candies[row][col].setpos(pos)
    candies[row][col].setheading(heading)

def is_neighbor(first_candy_row, first_candy_col, second_candy_row, second_candy_col):

    # This function checks whether two candies are next to each other
    # Input parameters, in this order, are:
    # - row of firstly-clicked candy
    # - column of firstly-clicked candy
    # - row of secondly-clicked candy
    # - column of secondly-clicked candy
    # It returns True (candies are next to each other) or False (candies are not next to each other)

    # If the clicked candies are in the same row, check whether their column numbers are adjacent
    if first_candy_row == second_candy_row and \
       (first_candy_col == second_candy_col - 1 or first_candy_col == second_candy_col + 1):
        return True

    # If the clicked candies are in the same column, check whether their row numbers are adjacent
    if first_candy_col == second_candy_col and \
       (first_candy_row == second_candy_row - 1 or first_candy_row == second_candy_row + 1):
        return True

    # If the clicked candies are not next to each other, the function returns False
    return False

def select_candies(x, y):

    # This function is run when any candies' turtle is clicked. It handles the swapping of candies
    # Input parameters: x, y
    # - the x, y coordinates of the clicked location

    global firstly_clicked_candy_row, firstly_clicked_candy_col, candy_map, first_candy_clicked

    # Get the row and column numbers of the clicked candy
    currently_clicked_candy_row = round((y - candy_pos[0][0][1]) / candy_size)
    currently_clicked_candy_col = round((x - candy_pos[0][0][0]) / candy_size)

    # If the player just clicked on the second candy (i.e. first_candy_clicked is already set to True)
    if first_candy_clicked:

        # If the clicked candies are next to each other
        if is_neighbor(firstly_clicked_candy_row, firstly_clicked_candy_col, currently_clicked_candy_row, currently_clicked_candy_col):
            # Swap the values of the two clicked candies in candy_map
            candy_map[firstly_clicked_candy_row][firstly_clicked_candy_col], candy_map[currently_clicked_candy_row][currently_clicked_candy_col] = \
                candy_map[currently_clicked_candy_row][currently_clicked_candy_col], candy_map[firstly_clicked_candy_row][firstly_clicked_candy_col]

            # If there is any matched group of candies handle the swapping and matching
            if len(find_any_matched_group()) > 0:
                swap_candies(firstly_clicked_candy_row, firstly_clicked_candy_col, currently_clicked_candy_row, currently_clicked_candy_col)
                display_candies()
                disable_clicking()
                turtle.ontimer(handle_matched_candies, delay)

            # If not, undo the swap
            else:
                candy_map[firstly_clicked_candy_row][firstly_clicked_candy_col], candy_map[currently_clicked_candy_row][currently_clicked_candy_col] = \
                    candy_map[currently_clicked_candy_row][currently_clicked_candy_col], candy_map[firstly_clicked_candy_row][firstly_clicked_candy_col]

        # Clear the candy highlight
        candies[firstly_clicked_candy_row][firstly_clicked_candy_col].clear()
        # Restore the variables to their original values, so that the player can select another pair of candies for swapping
        first_candy_clicked = False
        firstly_clicked_candy_row = -1
        firstly_clicked_candy_col = -1

    # If the player just clicked on the first candy (i.e. first_candy_clicked is False before clicking)
    else:
        # Store True in first_candy_clicked to indicate that the first candy is clicked
        first_candy_clicked = True
        # Store coordinates of the firstly-clicked candy in the corresponding variables
        firstly_clicked_candy_row = currently_clicked_candy_row
        firstly_clicked_candy_col = currently_clicked_candy_col
        # Highlight the candy
        highlight_candy(firstly_clicked_candy_row, firstly_clicked_candy_col)

def find_any_matched_group():

    # This function finds out a group of matched candies (i.e. 
    # "minimum_num_of_candies_required_for_matching" or more adjacent 
    # candies) and stores the results in the corresponding variables

    matched_group = []

    for row in range(num_of_candies_in_row):
        for col in range(num_of_candies_in_col):

            # No need to check if there is no candy here
            if candy(row, col) == nothing_in_cell:
                continue

            # Find the row below and above which matches the candy in a column
            matching_row_below = row
            while candy(row, col) == candy(matching_row_below, col):
                matching_row_below -= 1
            matching_row_above = row
            while candy(row, col) == candy(matching_row_above, col):
                matching_row_above += 1

            # If the candy is within a matching group, add it to the list
            if matching_row_above - matching_row_below - 1 >= minimum_num_of_candies_required_for_matching:
                matched_group.append((row, col))
                continue

            # Find the column on the left and right which matches the candy in a row
            matching_col_left = col
            while candy(row, col) == candy(row, matching_col_left):
                matching_col_left -= 1
            matching_col_right = col
            while candy(row, col) == candy(row, matching_col_right):
                matching_col_right += 1

            # If the candy is within a matching group, add it to the list
            if matching_col_right - matching_col_left - 1 >= minimum_num_of_candies_required_for_matching:
                matched_group.append((row, col))

    return matched_group

def eliminate_matched_candies():

    # This function eliminates the matched candies in candy_map

    global candy_map

    # Change the values in candy_map of the matched candies to nothing_in_cell
    for row, col in matched_group:
        candy_map[row][col] = nothing_in_cell

def update_score(num_of_matched_candies):

    # This function calculates the score and updates the score display
        
    global score

    # Calculate the new score
    score += num_of_matched_candies * 100

    # Clear the previous score and write the new one
    score_turtle.clear()
    score_turtle.goto(-220, -135)
    score_turtle.write("Score:", align="center", font=("Comic Sans MS", 16, "bold"))
    score_turtle.goto(-220, -175)
    score_turtle.write(str(score), align="center", font=("Comic Sans MS", 16, "bold"))

def move_candies_down_to_fill_gap():

    # This function moves candies down from the top to fill the gap ('empty' space)
    # produced by the matched candies which have just been eliminated

    global candy_map

    # Replace the 'empty' space with candies from above in a column
    for col in range(num_of_candies_in_col):
        # Find the first empty row from below
        start_empty_row = 0
        while candy(start_empty_row, col) != nothing_in_cell:
            start_empty_row += 1

        # Find the first empty row from above
        end_empty_row = num_of_candies_in_row - 1
        while candy(end_empty_row, col) != nothing_in_cell:
            end_empty_row -= 1

        # If there is a empty gap in the column
        if end_empty_row >= start_empty_row:
            rows_to_fill = end_empty_row - start_empty_row + 1
            for row in range(start_empty_row, num_of_candies_in_row):
                # Replace the space with candy from above
                candy_map[row][col] = candy(row + rows_to_fill, col)
                # Move the candy to prepare for the falling down animation
                candies[row][col].backward(candy_size * rows_to_fill)

    update_candy_type()
    display_candies()

    # Move the involved candies down with tracer set to True for the "new candies falling down from the top" animation
    turtle.tracer(True)
    for row in range(num_of_candies_in_row):
        for col in range(num_of_candies_in_col):
            pos = candies[row][col].pos()
            # If the candy is not in the correct position, move it
            if pos != candy_pos[row][row]:
                candies[row][col].goto(candy_pos[row][col])
    turtle.tracer(False)
                
def update_candy_type():

    # This function generates new candies for the 'empty' space in the candy_map

    global candy_map
    
    for row in range(num_of_candies_in_row):
        for col in range(num_of_candies_in_col):

            # Check if the candy is 'empty', and hence new candy generation is required
            if candy_map[row][col] == nothing_in_cell:

                # We generate a random number so that
                # 1) there is a 50% chance that we simply fill the empty space with any type of candy without any consideration (when rand is 0)
                # 2) there is a 50% chance that we generate a candy type with some consideration (refer to the following part) (when rand is 1)
                rand = random.randrange(2)

                # If rand equals to 1 (True)
                if rand:

                    # The following codes check whether there is a suitable candy type for candy_map[row][col] by
                    # checking the candy types of the candies around it. If a particular type of candy assigned can be
                    # swapped to any adjacent location to generate a matched group, we should assign that
                    # candy type to candy_map[row][col] to increase the number of possible matched groups 

                    if (candy(row-1, col-1) == candy(row-1, col+1)) and (candy(row-1, col-1) != -1):
                        candy_map[row][col] = candy(row-1, col-1)
                    elif (candy(row+1, col-1) == candy(row+1, col+1)) and (candy(row+1, col-1) != -1):
                        candy_map[row][col] = candy(row+1, col-1)
                        
                    elif (candy(row-2, col) == candy(row-3, col)) and (candy(row-2, col) != -1):
                        candy_map[row][col] = candy(row-2, col)
                    elif (candy(row+2, col) == candy(row+3, col)) and (candy(row+2, col) != -1):
                        candy_map[row][col] = candy(row+2, col)
                    elif (candy(row, col-2) == candy(row, col-3)) and (candy(row, col-2) != -1):
                        candy_map[row][col] = candy(row, col-2)
                    elif (candy(row, col+2) == candy(row, col+3)) and (candy(row, col+2) != -1):
                        candy_map[row][col] = candy(row, col+2)
                    
                    elif (candy(row-1, col-1) == candy(row-1, col-2)) and (candy(row-1, col-1) != -1):
                        candy_map[row][col] = candy(row-1, col-1)
                    elif (candy(row-1, col+1) == candy(row-1, col+2)) and (candy(row-1, col+1) != -1):
                        candy_map[row][col] = candy(row-1, col+1)
                    elif (candy(row+1, col-1) == candy(row+1, col-2)) and (candy(row+1, col-1) != -1):
                        candy_map[row][col] = candy(row+1, col-1)
                    elif (candy(row+1, col+1) == candy(row+1, col+2)) and (candy(row+1, col+1) != -1):
                        candy_map[row][col] = candy(row+1, col+1)

                    elif (candy(row-1, col-1) == candy(row-2, col-1)) and (candy(row-1, col-1) != -1):
                        candy_map[row][col] = candy(row-1, col-1)
                    elif (candy(row+1, col-1) == candy(row+2, col-1)) and (candy(row+1, col-1) != -1):
                        candy_map[row][col] = candy(row+1, col-1)
                    elif (candy(row-1, col+1) == candy(row-2, col+1)) and (candy(row-1, col+1) != -1):
                        candy_map[row][col] = candy(row-1, col+1)
                    elif (candy(row+1, col+1) == candy(row+2, col+1)) and (candy(row+1, col+1) != -1):
                        candy_map[row][col] = candy(row+1, col+1)

                    else:
                        # Just fill the space with any type of candy
                        candy_map[row][col] = random.randrange(num_of_candy_type)
                
                #If rand equals to 0 (False)
                else:
                    # Just fill the space with any type of candy
                    candy_map[row][col] = random.randrange(num_of_candy_type)

def display_candies():

    # This function updates the visual display of the candies

    for row in range(num_of_candies_in_row):
        for col in range(num_of_candies_in_col):

            # Change the shape of the turtle according to the candy type
            candies[row][col].shape(candy_image[candy(row, col)])
            
    turtle.update()

def enable_clicking():

    # This function enables the onclick event handlers of the 'candies' turtles

    global candies
    
    for row in range(num_of_candies_in_row):
        for col in range(num_of_candies_in_col):
            candies[row][col].onclick(select_candies)

def disable_clicking():

    # This function disables the onclick event handlers of the 'candies' turtles

    global candies
    
    for row in range(num_of_candies_in_row):
        for col in range(num_of_candies_in_col):
            candies[row][col].onclick(None)

def handle_matched_candies():

    # This function calls other functions to make an effect of
    # clearing the matched candies, moving down the candies to fill the
    # gap ('empty' space) created, generating new candies at the top 
    # and then displaying the new candies on the screen

    global matched_group

    if not end:
        matched_group = find_any_matched_group()
        num_of_matched_candies = len(matched_group)
        update_score(num_of_matched_candies)
        eliminate_matched_candies()
        move_candies_down_to_fill_gap()

        # Check if there is any more matched group
        # If yes, call this function again for further processing
        # of those matched groups 
        if len(find_any_matched_group()) > 0:
            turtle.ontimer(handle_matched_candies, delay)
        else:
            enable_clicking()

def game_over():

    # This function disables the click events of the 'candies' turtles and shows a message when the game is over

    global end

    end = True

    message = "Your final score was " + str(score) + "!"

    turtle.up()
    turtle.goto(1, -2)
    turtle.pencolor("black")
    turtle.write(message, align="center", font=("Arial", 30, "bold"))
    turtle.goto(0, 0)
    turtle.pencolor("white")
    turtle.write(message, align="center", font=("Arial", 30, "bold"))

    disable_clicking()

def start_game(x, y):

    # This function is called when the player clicks on the start button to start the game
    # It calls other functions for preparing and starting the game

    # Clear the instruction screen first
    instruction_turtle.clear()
    instruction_turtle.pencolor("gray20")
    instruction_turtle.goto(-220, -25)
    instruction_turtle.write("Time:", align="center", font=("Comic Sans MS", 16, "bold"))
    turtle.onscreenclick(None)

    # Then, call other functions to start the game
    generate_candies_turtles()
    generate_candy_map()
    display_candies()
    enable_clicking()
    countdown()
    update_score(0)
    
# The following is for drawing the instruction screen with a start button

# Hide the default turtle
turtle.hideturtle()

# Write the game instructions with shadow
def write_instruction(offsetx, offsety, color):
    instructions = [["Remove candies by matching three or",
                     "more candies of the same colour in",
                     "either a row or a column"],
                    ["Swap any two adjacent candies by",
                     "clicking on them"],
                    ["The larger number of matched candies",
                     "the higher mark you get"]]
    instruction_turtle.goto(-120 + offsetx, 160 + offsety)
    instruction_turtle.color(color)
    for instruction in instructions:
        for line in instruction:
            instruction_turtle.write(line, font=("Comic Sans MS", 15, "bold"))
            instruction_turtle.sety(instruction_turtle.ycor() - 30)
        instruction_turtle.sety(instruction_turtle.ycor() - 20)
    instruction_turtle.goto(70, instruction_turtle.ycor() - 30)
    instruction_turtle.write("Click anywhere on", align="center", font=("Comic Sans MS", 20, "bold"))
    instruction_turtle.sety(instruction_turtle.ycor() - 40)
    instruction_turtle.write("the screen to start!", align="center", font=("Comic Sans MS", 20, "bold"))
instruction_turtle = turtle.Turtle()
instruction_turtle.up()
instruction_turtle.hideturtle()
write_instruction(1, -2, "black")
write_instruction(0, 0, "yellow")

# Set up the event handler for the game start
turtle.onscreenclick(start_game)

# Update the screen to show everything we instructed the turtle to draw so far
turtle.update()

# The player can now interact with the game interface via the event handlers to play the game
turtle.done()
