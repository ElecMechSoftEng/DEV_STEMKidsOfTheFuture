# Python Pong Game

import turtle

# Windows
wn = turtle.Screen()
wn.title("Pong By CloudSpace")
wn.bgcolor("black")
wn.setup(width=800, height=600)     # Size of screen in pixel dimentions
wn.tracer(0)                        # Helps with refresh rate of window

# Main Game Loop
while True:
    wn.update()
