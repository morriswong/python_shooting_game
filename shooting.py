"""
    Turtle Graphics - Shooting Game
"""

import turtle

"""
    Constants and variables
"""
screen_width, screen_height = 900, 564


turtle.reset()                              # Reset the turtle
turtle.setup(screen_width, screen_height)   # Set the size of the screen
turtle.bgpic("Hogwarts-castle-harry-potter.gif")               # Put the background image on the
                                            # screen
turtle.width(2)                             # Draw lines with a width of tw



# General parameters
window_height = 600
window_width = 600
window_margin = 50
update_interval = 25    # The screen update interval in ms, which is the
                        # interval of running the updatescreen function

# Player's parameters
player_size = 50        # The size of the player image plus margin
player_init_x = 0
player_init_y = -window_height / 2 + window_margin
player_speed = 10       # The speed the player moves left or right

# Enemy's parameters
enemy_number = 10       # The number of enemies in the game

enemy_size = 50         # The size of the enemy image plus margin
enemy_init_x = -window_width / 2 + window_margin
enemy_init_y = window_height / 2 - window_margin
enemy_min_x = enemy_init_x
enemy_max_x = window_width / 2 - enemy_size * min(6, enemy_number)
    # The maximum x coordinate of the first enemy, which will be used
    # to restrict the x coordinates of all other enemies
enemy_hit_player_distance = 30
    # The player will lose the game if the vertical
    # distance between the enemy and the player is smaller
    # than this value

# Enemy movement parameters
enemy_speed = 2
enemy_speed_increment = 1
    # The increase in speed every time the enemies move
    # across the window and back
enemy_direction = 1
    # The current direction the enemies are moving:
    #     1 means from left to right and
    #     -1 means from right to left

# The list of enemies
enemies = []

# Laser parameter
laser_width = 2
laser_height = 15
laser_speed = 20
laser_hit_enemy_distance = 20
    # The laser will destory an enemy if the distance
    # between the laser and the enemy is smaller than
    # this value

"""
    Handle the player movement
"""

# This function is run when the "Left" key is pressed. The function moves the
# player to the left when the player is within the window area
def playermoveleft():

    # Get current player position
    x, y = player.position()

    # Part 2.2 - Keeping the player inside the window
    # Player should only be moved only if it is within the window range

    if x - player_speed > -window_width / 2 + window_margin:
        player.goto(x - player_speed, y)

    turtle.update() # delete this line after finishing updatescreen()

# This function is run when the "Right" key is pressed. The function moves the
# player to the right when the player is within the window area
def playermoveright():

    # Get current player position
    x, y = player.position()

    # Part 2.2 - Keeping the player inside the window
    # Player should only be moved only if it is within the window range

    if x + player_speed < window_width / 2 - window_margin:
        player.goto(x + player_speed, y)

    turtle.update() # delete this line after finishing updatescreen()

"""
    Handle the screen update and enemy movement
"""

# This function is run in a fixed interval. It updates the position of all
# elements on the screen, including the player and the enemies. It also checks
# for the end of game conditions.
def updatescreen():
    # Use the global variables here because we will change them inside this
    # function
    global enemy_direction, enemy_speed

    # Move the enemies depending on the moving direction

    # The enemies can only move within an area, which is determined by the
    # position of enemy at the top left corner, enemy_min_x and enemy_max_x

    # x and y displacements for all enemies
    dx = enemy_speed * enemy_direction
    dy = 0

    # Part 3.3
    # Perform several actions if the enemies hit the window border
    x0 = enemies[0].xcor()
    if x0 + dx > enemy_max_x or x0 + dx < enemy_min_x:
    # Perform several action when the enemies hit the window border
    
        # Switch the moving direction
        enemy_direction = -enemy_direction
        # Bring the enemies closer to the player
        dy = -enemy_size / 2
        # Increase the speed when the direction switches to right again
        if enemy_direction == 1:
            enemy_speed = enemy_speed + enemy_speed_increment    
    # Move the enemies according to the dx and dy values determined above
    for enemy in enemies:
        x, y = enemy.position()
        enemy.goto(x + dx, y + dy)

        if (x // 20) % 2 == 0:
            enemy.shape("voldemort1.gif")
        else:
            enemy.shape("voldemort2.gif")

    # Part 4.3 - Moving the laser
    # Perfrom several actions if the laser is visible

    if laser.isvisible():
        # Move the laser
        x, y = laser.position()
        laser.goto(x,y + laser_speed)
        # Hide the laser if it goes beyong the window
        if laser.ycor() > window_height / 2:
            laser.hideturtle()
    # Check the laser against every enemy using a for loop
        for enemy in enemies:
            # If the laser hits a visible enemy, hide both of them
            if enemy.isvisible() and laser.distance(enemy)<laser_hit_enemy_distance:
                #hide enemy
                enemy.hideturtle()
                #hide laser
                laser.hideturtle()
                # Stop if some enemy is hit
                break

    # Part 5.1 - Gameover when one of the enemies is close to the player

    # If one of the enemies is very close to the player, the game will be over
    for enemy in enemies:
        if enemy.ycor()-player.ycor() < enemy_hit_player_distance and enemy.isvisible(): 
            # Show a message
            gameover("You lose!")

            # Return and do not run updatescreen() again
            return

    # Part 5.2 - Gameover when you have killed all enemies

    # Set up a variable as a counter
    count = 0
    # For each enemy
    for enemy in enemies:
        # Increase the counter if the enemy is visible
        if enemy.isvisible():
            count = count +1 
    # If the counter is 0, that means you have killed all enemies
    if count == 0:
        # Show a message
        gameover("You win!")

        # Return and do not run updatescreen() again
        return
        
        # Perform several gameover actions

    # Part 3.1 - Controlling animation using the timer event

    #
    # Add code here
    #

    # Update the screen
    turtle.update()

    # Schedule the next screen update
    turtle.ontimer(updatescreen, update_interval)

"""
    Shoot the laser
"""

# This function is run when the player presses the spacebar. It shoots a laser
# by putting the laser in the player's current position. Only one laser can
# be shot at any one time.
def shoot():

    print("Pyoo!") # delete this line after completing the function

    # Part 4.2 - the shooting function
    # Shoot the laser only if it is not visible
    if not laser.isvisible():
    #
    # Add code here
    #
        # Make the laser to become visible
        laser.showturtle()
        # Move the laser to the position of the player
        x, y = player.position()
        laser.goto(x,y)    

"""
    Game start
"""
# This function contains things that have to be done when the game starts.
def gamestart(x,y):
    # Use the global variables here because we will change them inside this
    # function
    global player, laser

    start_button.clear()
    start_button.hideturtle()

    #hw 3.4
    labels.clear()
    enemy_number_rarrow.hideturtle()
    enemy_number_larrow.hideturtle()
    enemy_number_text.clear()

    ### Player turtle ###

    # Add the spaceship picture
    turtle.addshape("harrypotter.gif")

    # Create the player turtle and move it to the initial position
    player = turtle.Turtle()
    player.shape("harrypotter.gif")
    player.up()
    player.goto(player_init_x, player_init_y)

    # Part 2.1
    # Map player movement handlers to key press events

    turtle.onkeypress(playermoveleft, "Left")
    turtle.onkeypress(playermoveright, "Right")

    turtle.listen() 

    #
    # Add code here
    #

    ### Enemy turtles ###

    # Add the enemy picture
    turtle.addshape("voldemort1.gif")
    turtle.addshape("voldemort2.gif")

    enemy_max_x = window_width / 2 - enemy_size * min(6, enemy_number)

    for i in range(enemy_number):
        # Create the turtle for the enemy
        enemy = turtle.Turtle()
        enemy.shape("voldemort1.gif")
        enemy.up()

        # Move to a proper position counting from the top left corner
        enemy.goto(enemy_init_x + enemy_size * (i % 6), enemy_init_y - enemy_size * (i // 6))
        # Add the enemy to the end of the enemies list
        enemies.append(enemy)

    ### Laser turtle ###

    # Create the laser turtle using the square turtle shape
    laser = turtle.Turtle()
    laser.shape("square")
    laser.color("White")

    # Change the size of the turtle and change the orientation of the turtle
    laser.shapesize(laser_width / 20, laser_height / 20)
    laser.left(90)
    laser.up()

    #laser.goto(player.xcor(), player.ycor())

    # Hide the laser turtle
    laser.hideturtle()

    # Part 4.2 - Mapping the shooting function to key press event

    #
    # Add code here
    #

    turtle.onkeypress(shoot, "space")

    turtle.update()

    # Part 3.1 - Controlling animation using the timer event

    #
    # Add code here
    #

    # Start the game by running updatescreen()
    turtle.ontimer(updatescreen, update_interval)


"""
    Game over
"""

# This function shows the game over message.
def gameover(message):

    # Part 5.3 - Improving the gameover() function

    #print(message) # delete this line after completing the function

    text = turtle.Turtle()
    text.hideturtle()
    text.pencolor("yellow")
    text.write(message, align="center", font=("System", 30, "bold"))
    turtle.update()


"""
    Set up main Turtle parameters
"""

# Set up the turtle window
turtle.setup(window_width, window_height)
turtle.bgcolor("Black")
turtle.up()
turtle.hideturtle()
turtle.tracer(False)

# Start the game
#gamestart()

# Set up the start_button

start_button = turtle.Turtle()
start_button.onclick(gamestart)

start_button.up()
start_button.goto(-40, -40)
start_button.color("White", "DarkGray")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(80)
    start_button.left(90)
    start_button.forward(25)
    start_button.left(90)
start_button.end_fill()

start_button.color("White")
start_button.goto(0, -35)
start_button.write("Start", font=("System", 12, "bold"), align="center")

start_button.color("")
start_button.goto(0, -28)
start_button.shape("square")
start_button.shapesize(1.25, 4)

# Set up other controls

labels = turtle.Turtle()
labels.hideturtle()
labels.color("white")
labels.up()
labels.goto(-100, 0) # Put the text next to the spinner control
labels.write("Number of Enemies:", font=("System", 12, "bold"))

enemy_number_text = turtle.Turtle()
enemy_number_text.up()
enemy_number_text.hideturtle()
enemy_number_text.color("white")
enemy_number_text.goto(80,0) # may need to rearrange

enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")

enemy_number_larrow = turtle.Turtle()
enemy_number_larrow.color("white")
enemy_number_larrow.up()
enemy_number_larrow.goto(60,8)
enemy_number_larrow.shape("arrow")
enemy_number_larrow.shapesize(0.5,1)
enemy_number_larrow.left(180)

enemy_number_rarrow = turtle.Turtle()
enemy_number_rarrow.color("white")
enemy_number_rarrow.up()
enemy_number_rarrow.goto(100,8)
enemy_number_rarrow.shape("arrow")
enemy_number_rarrow.shapesize(0.5,1)
enemy_number_rarrow.right(0)

def decrease_enemy_number(x, y):
    global enemy_number
    if enemy_number > 1 :
        # decrease number of enemies by 1
        enemy_number = enemy_number - 1
        # tell the turtle 'enemy_number_text' to clear what it has written
        enemy_number_text.clear()
        # tell the turtle 'enemy_number_text' to display the new value
        enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")

# right arrow, 3.3
def increase_enemy_number(x, y):
    # Declare enemy_number as global
    global enemy_number
    if enemy_number < 48 :
        # increase number of enemies by 1
        enemy_number = enemy_number + 1 
        # tell the turtle 'enemy_number_text' to clear what it has written
        enemy_number_text.clear()
        # tell the turtle 'enemy_number_text' to display the new value
        enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")


enemy_number_larrow.onclick(decrease_enemy_number)
enemy_number_rarrow.onclick(increase_enemy_number)


turtle.update()

# Switch focus to turtle graphics window
turtle.done()
