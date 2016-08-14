#!/usr/bin/env python
import turtle
import random

def bloom(radius):
    turtle.colormode(255)
    
    for rad in range (40, 10, -5):
        for iter in range(360//rad):
            turtle.up()
            turtle.circle(radius+rad,rad)
            turtle.begin_fill();
            turtle.fillcolor((200+random.randint(0,rad),
                              200+random.randint(0,rad),
                              200+random.randint(0,rad)))
            turtle.down()
            turtle.circle(-rad)
            turtle.end_fill();

            

turtle.speed(0)
turtle.colormode(1.0)
bloom(5)
turtle.exitonclick()
