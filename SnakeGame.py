#       IMPORTANT
#   This program and my 2 classes were debugged using Google Gemini,
#   No features were coded using ai, only debugging since there were numerous syntax errors plagueing this program
import turtle as t
import time
import random
import winsound
import snakebot
from food import Food
from snake import Snake
from snakebot import Snakebot

#Global Variables
controliterator = 0
delay = 0.1
wn = t.Screen()
wn.title("Snake Game")
wn.bgcolor("ivory4")
wn.setup(width=600, height=600)
wn.tracer(0) # This prevents the flickering/freezing during updates
food = Food()
snake = Snake()
bot = Snakebot()
bot_moving = False
controldrawer = t.Turtle()
scoreboarddrawer = t.Turtle()

def drawscoreboard():
    scoreboarddrawer.penup()
    scoreboarddrawer.goto(0, 400)
    scorename = wn.textinput(title="What is your name? ", prompt="Type your name... ")
    scoreboarddrawer.write(scorename, font=("Arial", 20, "normal"))
    scoreboarddrawer.hideturtle()
def drawcontrols():
    controldrawer.penup()
    controldrawer.goto(-700,-400)
    controldrawer.pendown()
    controldrawer.write(f"W = Forward\nA = Left\nS = Backwards\nD = Right", font=("Arial", 20, "normal"))
    controldrawer.hideturtle()
def reset_game():
    time.sleep(1)
    snake.head.goto(0, 0)
    snake.head.direction = "stop"
    # Hide the old body parts before clearing the list
    for part in snake.body_parts:
        part.goto(1000, 1000) 
    snake.body_parts.clear()

# Bind keys directly to the snake object methods
wn.listen()
wn.onkeypress(snake.up, "w")
wn.onkeypress(snake.down, "s")
wn.onkeypress(snake.left, "a")
wn.onkeypress(snake.right, "d")

while True:
    wn.update() # Manually refresh the screen for smoothness

    # Wall collisions
    if (snake.head.xcor() > 290 or snake.head.xcor() < -290 or 
        snake.head.ycor() > 290 or snake.head.ycor() < -290):
        reset_game()

    if bot_moving:
        bot.update_direction()
    # Food collisions
    if bot.head.distance(food) < 20:
        fx,fy=food.refresh()
        bot.fx = fx
        bot.fy = fy
        bot.update_direction()
        bot_moving = True
        newbot_segment = t.Turtle("square")
        newbot_segment.penup()
        newbot_segment.color("grey")
        bot.body_parts.append(newbot_segment)
    elif snake.head.distance(food) < 20:
        fx,fy=food.refresh()
        bot.fx = fx
        bot.fy = fy
        bot.update_direction()
        bot_moving = True
        new_segment = t.Turtle("square")
        new_segment.penup()
        new_segment.color("grey")
        snake.body_parts.append(new_segment)
        #color logic found on stack overflow: https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
        r = lambda: random.randint(0,255)
        snakeheadcolor = '#%02X%02X%02X' % (r(),r(),r())
        snakebodycolor = '#%02X%02X%02X' % (r(),r(),r())
        snake.head.color(snakeheadcolor)
        winsound.PlaySound("Assets/eating.wav", winsound.SND_FILENAME)

    # Move body segments
    for i in range(len(snake.body_parts) - 1, 0, -1):
        x = snake.body_parts[i-1].xcor()
        y = snake.body_parts[i-1].ycor()
        snake.body_parts[i].goto(x, y)

    if len(snake.body_parts) > 0:
        snake.body_parts[0].goto(snake.head.xcor(), snake.head.ycor())
        
    # Bot body segments
    for i in range(len(bot.body_parts) - 1, 0, -1):
        x = bot.body_parts[i-1].xcor()
        y = bot.body_parts[i-1].ycor()
        bot.body_parts[i].goto(x, y)

    if len(bot.body_parts) > 0:
        bot.body_parts[0].goto(bot.head.xcor(), bot.head.ycor())
    snake.move()
    

    # Body collisions
    for part in snake.body_parts:
        if part.distance(snake.head) < 10:
            reset_game()
            
    while controliterator == 0:
        print("""
            (W) - Forward
            (A) - Left
            (S) - Down
            (D) - Right
            """)
        controliterator = controliterator + 1
        drawcontrols()
        drawscoreboard()
    time.sleep(delay)