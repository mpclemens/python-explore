#!/usr/bin/env python3
"""
Draw a fractal tree
"""

import turtle
import random
    
class Tree:
    
    MAX_BRANCH = 5; # 2..N branches per joint
    MAX_DEPTH  = 4; # maximum number of recursive iterations (branches)
    
    def __init__(self):
        self.segments = []
        self._points  = []

    def draw(self, trunk = 100):
        """Draw the tree with the given turtle object, as the current point.
        The turtle's original orientation will be preserved on exit, and 
        the turtle will be placed at the original point on completion. Current 
        pen size and color will be used to draw the tree.

        If the tree has been drawn once before, then it will be
        overdrawn using the same points. Otherwise, create the tree
        and store the points of the segments in the `segments[]` list.
        """
        _restore_heading = turtle.heading()
        _restore_pos     = turtle.pos()
        _restore_pen     = turtle.pen()
        
        turtle.setheading(90) # due north

        # Determine the points if there's none set yet.
        # The segment length determines the depth of iterations.

        turtle.pendown()
        self._trunk = trunk
        self._draw_segments(start_point = _restore_pos,
                            iteration = 0,
                            save_points = len(self.segments) == 0)
        turtle.penup()

        turtle.setheading(_restore_heading)
        turtle.setposition(_restore_pos)
        turtle.pen(_restore_pen)

    def _draw_segments(self, start_point, iteration, save_points):
        """Helper method to draw the tree, either from new points or from
        stored ones, until the segment bounding box is smaller than the
        limit stored with the class"""

        if (iteration > Tree.MAX_DEPTH):
            return;

        if (save_points):
            self._points.append(turtle.pos())
                
        if (iteration == 0):
            # Trunk, always draw
            turtle.forward(self._trunk)
            if (save_points):
                self._points.append(turtle.pos())                
            self._draw_segments(turtle.pos(), iteration+1, save_points)
            
        else:
            # Assuming the current branch (segment) is the middle of a
            # forked branch, the sub-branches growing from its end are
            # either the current heading minus a few degrees (a relative
            # right turn), or the current heading plus a few degrees (a
            # relative left). About half the branches should land on
            # either side.
            #
            # Determine the new heading by deciding how many
            # branches are going to be growing, and then add or
            # subtract an amount from the turtle's original angle.
            #                
            branches      = random.randint(2,Tree.MAX_BRANCH + 1);
            start_heading = turtle.heading()
            start_pos     = turtle.pos()
        
            for branch in range(branches):
                turtle.penup()
                turtle.setpos(start_pos)
                turtle.setheading(start_heading)
                turtle.pendown()
                if (branch <= branches/2):
                    turtle.right(random.randint(15,20) * branch)
                else:
                    turtle.left(random.randint(15,20) * branch)
                    
                turtle.forward(self._trunk/(iteration+1))
                self._draw_segments(turtle.pos(), iteration+1, save_points)

###

my_tree = Tree()
turtle.speed(0)
turtle.home()
my_tree.draw(100)
turtle.write("Click in window to close")
turtle.exitonclick()
# print(my_tree._points)
