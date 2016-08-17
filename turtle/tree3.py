#!/usr/bin/env python3
"""
Draw a fractal tree and friends
"""

from turtle import (Turtle, exitonclick)
from Tree import Tree

###

my_turtle = Turtle()
my_turtle.hideturtle()
my_turtle.speed(0)
my_turtle.home()
my_turtle.pencolor("green")
my_turtle.pensize(2)

# a big tree
my_tree = Tree()
my_tree.draw(my_turtle, trunk=100, max_depth=5)

# a slightly smaller tree
my_turtle.penup()
my_turtle.goto(175,30)
my_tree = Tree()
my_tree.draw(my_turtle, trunk=80, max_depth=4)

# a Charlie Brown tree
my_turtle.penup()
my_turtle.goto(-150,40)
my_tree = Tree()
my_tree.draw(my_turtle, trunk=40, max_depth=2)

my_turtle.penup()
my_turtle.goto(0,-50)
my_turtle.write("Click in window to close")

exitonclick()
