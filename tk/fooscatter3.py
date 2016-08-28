#!/usr/bin/env python3

import random
import tkinter
import time

WIDTH = 400
HEIGHT = 450

tk = tkinter.Tk()
canvas = tkinter.Canvas(tk, width=WIDTH, height=HEIGHT)
canvas.pack()

def randcolor():
    return random.choice(['white', 'black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta'])

for i in range(100):
    canvas.create_text(random.randrange(i,WIDTH),
                       random.randrange(i,HEIGHT),
                       text="Foo", fill=randcolor())
    
tkinter.mainloop()
    
