# Python Pong Game

import turtle

# Windows
wn = turtle.Screen()
wn.title("Pong By CloudSpace")
wn.bgcolor("black")
wn.setup(width=800, height=600)     # Size of screen in pixel dimentions
wn.tracer(0)                        # Helps with refresh rate of window

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)  # Max Speed of Animation
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0) # Initial position


# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)  # Max Speed of Animation
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0) # Initial position


# Ball


# Main Game Loop
while True:
    wn.update()