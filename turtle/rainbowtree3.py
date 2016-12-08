#!/usr/bin/env python3
"""
Draw a rainbow tree, for T
"""

from turtle import (Turtle, exitonclick)
from Tree import Tree

###

def main():
    """Cycles through pen colors and sizes to overdraw a fractal tree"""
    my_turtle = Turtle()
    my_turtle.hideturtle()
    my_turtle.speed(0)
    my_turtle.penup()
    my_turtle.goto(0, -100)

    my_tree = Tree()
    inks = ["purple", "blue", "green", "yellow", "orange", "red"]
    my_turtle.pensize(len(inks) * 2 + 1)

    for ink in inks:
        my_turtle.pencolor(ink)
        my_tree.draw(my_turtle, trunk=150, max_depth=4)
        my_turtle.pensize(my_turtle.pensize() - 2)

###

if __name__ == "__main__":
    main()
    exitonclick()
