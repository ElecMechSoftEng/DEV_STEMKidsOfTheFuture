# Python Pong Game
import turtle
import pygame
from pygame import mixer

# Windows
wn = turtle.Screen()
wn.title("Pong By CloudSpace")
wn.bgcolor("black")
wn.setup(width=800, height=600)     # Size of screen in pixel dimensions
wn.tracer(0)                        # Helps with refresh rate of window

# Score
score_a = 0
score_b = 0

# Sounds and Music
mixer.init()
mixer.music.load('bounce.wav')

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)  # Max Speed of Animation
paddle_a.shape("square")  # sets OG dimensions  of wide100 x tall100
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)  # mods OG dims by height+5 and width+0
paddle_a.penup()
paddle_a.goto(-350, 0)  # Initial position


# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)  # Max Speed of Animation
paddle_b.shape("square")  # sets OG dimensions  of 1x1
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1) # mods OG dims by height+5 and width+0
paddle_b.penup()
paddle_b.goto(350, 0)  # Initial position


# Ball
ball = turtle.Turtle()
ball.speed(0)  # Max Speed of Animation
ball.shape("square")  # sets OG dimensions  of 1x1
ball.color("white")
ball.penup()
ball.goto(0, 0)  # Initial position
ball.dx = 0.1     # ball delta move or change
ball.dy = -0.1     # Moves by 2

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player 1: 0  Player 2: 0", align="center", font=("Courier", 24, "normal"))


# Function
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


# Keyboard Binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

# Main Game Loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border Checking
    if ball.ycor() > 290:   # Top Border
        ball.sety(290)
        mixer.music.play()
        ball.dy *= -1


    if ball.ycor() < -290:  # Bottom Border
        ball.sety(-290)
        mixer.music.play()
        ball.dy *= -1


    if ball.xcor() > 390:   # Right Border
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player 1: {}  Player 2: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    if ball.xcor() < -390:  # Left Border
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player 1: {}  Player 2: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    # Paddle and Ball Collisions
    if ((ball.xcor() > 340) and (ball.xcor() < 350)) and ((ball.ycor() < paddle_b.ycor() + 40) and (ball.ycor() > paddle_b.ycor() - 40)):
        ball.setx(340)
        mixer.music.play()
        ball.dx *= -1

    if ((ball.xcor() < -340) and (ball.xcor() > -350)) and ((ball.ycor() < paddle_a.ycor() + 40) and (ball.ycor() > paddle_a.ycor() - 40)):
        ball.setx(-340)
        mixer.music.play()
        ball.dx *= -1
