#!/usr/bin/env python3
"""Draw a fractal tree using turtle graphics"""

import random

class Tree:
    
    def __init__(self):
        self.segments = []    # for redrawing/overdrawing
        self._points  = set() # all vertices

    def draw(self, my_turtle, trunk = 100, max_depth = 4):
        """Draw the tree with the given turtle object, as the current point.
        The turtle's original orientation will be preserved on exit, and 
        the turtle will be placed at the original point on completion. Current 
        pen size and color will be used to draw the tree.

        If the tree has been drawn once before, then it will be
        overdrawn using the same points. Otherwise, create the tree
        and store the points of the segments in the `segments[]` list.
        """
        _restore_heading = my_turtle.heading()
        _restore_pos     = my_turtle.pos()
        _restore_pen     = my_turtle.pen()
        
        my_turtle.setheading(90) # due north

        # Determine the points if there's none set yet.
        # The segment length determines the depth of iterations.

        my_turtle.pendown()
        self._trunk = trunk
        self._draw_segments(start_point = _restore_pos,
                            my_turtle = my_turtle,
                            iteration = 0,
                            max_depth = max_depth,
                            save_points = len(self.segments) == 0)
        my_turtle.penup()

        my_turtle.setheading(_restore_heading)
        my_turtle.setposition(_restore_pos)
        my_turtle.pen(_restore_pen)

    def _draw_segments(self, my_turtle, start_point, iteration, max_depth, save_points):
        """Helper method to draw the tree, either from new points or from
        stored ones, until the segment bounding box is smaller than the
        limit stored with the class"""

        if (iteration > max_depth):
            return;
                
        if (iteration == 0):
            # Trunk, always draw
            if (save_points):
                self._points.add(start_point)
            my_turtle.forward(self._trunk)
            if (save_points):
                self.segments.append((start_point, my_turtle.pos()))
                self._points.add(my_turtle.pos())                
            self._draw_segments(my_turtle = my_turtle,
                                start_point = my_turtle.pos(),
                                iteration = iteration+1,
                                max_depth = max_depth,
                                save_points = save_points)
            
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
            branches      = random.randint(2,5);
            min_angle     = 75//branches
            max_angle     = 90//branches
            start_heading = my_turtle.heading()
            start_pos     = my_turtle.pos()
        
            for branch in range(branches):
                my_turtle.penup()
                my_turtle.setpos(start_pos)
                my_turtle.setheading(start_heading)
                my_turtle.pendown()
                if (branch <= branches/2):
                    my_turtle.right(random.randint(min_angle,max_angle) * branch)
                else:
                    my_turtle.left(random.randint(min_angle,max_angle) * branch)
                    
                my_turtle.forward(self._trunk/(iteration+1))
                if (save_points):
                    self.segments.append((start_point, my_turtle.pos()))
                    self._points.add(my_turtle.pos())                

                self._draw_segments(my_turtle = my_turtle,
                                    start_point = my_turtle.pos(),
                                    iteration = iteration+1,
                                    max_depth = max_depth,
                                    save_points = save_points)


###

import unittest
from turtle import Turtle

class TestTree(unittest.TestCase):
    
    def test_initialize(self):
        my_turtle = Turtle()
        my_tree = Tree()

        self.assertEqual(len(my_tree.segments),0,"No segments stored")
        # whitebox
        self.assertEqual(len(my_tree._points),0,"No points stored")

    def test_points_stored(self):
        my_turtle = Turtle()
        my_turtle.speed(0)
        my_tree = Tree()
        my_tree.draw(my_turtle, max_depth = 1)        
        # whitebox

        self.assertTrue(len(my_tree._points) > 0,"Some points should be stored")
    
    def test_segments_stored(self):
        my_turtle = Turtle()
        my_turtle.speed(0)
        my_tree = Tree()
        my_tree.draw(my_turtle, max_depth = 1)

        self.assertTrue(len(my_tree.segments) > 0,"Some segments should be stored")
        
    
if (__name__ == "__main__"):
    unittest.main()
