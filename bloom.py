#!/usr/bin/env python
import turtle
import random

def bloom(radius):
    for iter in range(18):
        turtle.circle(radius,20)
        turtle.begin_fill();
        turtle.fillcolor(random.random(),random.random(),random.random())
        turtle.circle(-radius/5)
        turtle.end_fill();


turtle.speed(0)
turtle.colormode(1.0)
bloom(100)
turtle.exitonclick()
