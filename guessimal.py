#!/usr/bin/env python

import pickle # to serialize/unserialize the data file

# Class to represent a binary tree of clues with leaf nodes representing
# animals
#
class Node:

        def __init__(self, my_text, parent_node=None, parent_answer=None):
                """Optionally attach a new node to a parent's Y or N answer"""
                self.text = my_text
                self.children = {}
                if (None != parent_node and None != parent_answer):
                        parent_node.set_child(self,parent_answer)
                        
        def is_leaf(self):
                """Returns True if the current node is a leaf"""
                return(None == self.children or 0 == len(self.children.keys()))

        def set_child(self, child_node, my_answer):
                """Hook a new node under the current one, at the answer point"""
                self.children[my_answer] = child_node

        def get_child(self, my_answer):
                """Return the child hung from the answer, if any, or None"""
                if (None == self.children or my_answer not in self.children):
                        return(None)
                else:
                        return(self.children[my_answer])

        @classmethod
        def init_tree(class_name):
                """Initialize a simple guess tree for the first time the game is run"""
                root_node = Node("has four legs")
                # "y" branch of the root node (has four legs)
                pet_node = Node("is a house pet",root_node,"y")
                Node("a dog",pet_node,"y")
                Node("a komodo dragon",pet_node,"n")
                # "n" branch of the root node (does not have four legs)
                wing_node = Node("has wings",root_node,"n")
                Node("a raven",wing_node,"y")
                Node("a garter snake",wing_node,"n")

                return(root_node)


        @classmethod
        def load_tree(class_name, file_name):
                """Load a tree, or on failure, use a default tree from the class"""
                if (None != file_name):
                        # Try loading from the supplied file
                        try:
                                data_file = open(file_name,"rb")
                                root_node = pickle.load(data_file)
                        except IOError:
                                # bad things happened, so just return the default tree
                                root_node = Node.init_tree()
                else:
                        root_node = Node.init_tree()
                return root_node

        
        def save_tree(self, file_name):
                """Archive the tree for future games"""
                try:
                        data_file = open(file_name,"w")
                        pickle.dump(self, data_file, 0) # using ASCII save protocol
                except IOError as e:
                        print("ERROR: could not save data file")
                        raise e

###

class Guessimal:
        
        def __init__(self, file_name="guessimal.data"):
                """Begin a new game, loading from a file"""
                self.data_file = file_name
                self.root_node = Node.load_tree(self.data_file)

        def input_yes_no(self,prompt_text):
                """Centralized Y/N handler for user input"""
                try:
                        # Python 2
                        user_input = raw_input(prompt_text + " (Y/N) ")
                except NameError:
                        # Python 3
                        user_input = input(prompt_text + " (Y/N) ")

                # first character, lower-cased to make comparison easier
                user_input = user_input.lstrip().lower()
                return user_input[0]
                

        def input_text(self, prompt_text):
                try:
                        # Python 2
                        user_input = raw_input(prompt_text)
                except NameError:
                        # Python 3
                        user_input = input(prompt_text)
                        
                # lop off leading and trailing whitespace
                user_input = user_input.lstrip().rstrip()
                return user_input    


        def process_node(self, current_node):
                """Handle each node appropriately: leaves are animals, others are clues"""
                if (current_node.is_leaf()):
                        # Found an animal...
                        user_response = self.input_yes_no("Is your animal " + current_node.text + "?")
                        # but if it's the wrong one, then the tree gets extended
                        if ('n' == user_response):
                                self.add_clue(self.previous_clue, self.previous_response, current_node)
                                print("Thanks! I'm saving the clues for next time.")
                                self.root_node.save_tree(self.data_file)
                        else:
                                print("I am very clever! YAY ME!")
                                
                else:
                        # Found a clue, so ask it and recurse into the subtree
                        self.previous_clue = current_node # needed when we add an animal (parent of new leaf node)
                        
                        user_response = self.input_yes_no("Your animal " + current_node.text + "?")
                        self.previous_response = user_response

                        self.process_node(current_node.get_child(user_response))

        # The user is too clever! Add a new clue and animal in the tree that differentiates it from the
        # bad guess
        def add_clue(self, parent_node, parent_response, wrong_animal):
                print(
"""
OK, you stumped me. Tell me the animal you were thinking of so I can learn it.

Be sure to add "a" or "an" in front of the animal's name, like "a giraffe"
""")

                animal_reply = 'n'
                while ('y' != animal_reply):
                        animal_text = self.input_text("Your animal is: ")
                        animal_reply = self.input_yes_no("Your animal is " + animal_text + ", is this OK?")
                
                print("Now I need to know what makes", animal_text, "different from", wrong_animal.text)
                print("Please finish this clue:")

                clue_reply = 'n'
                while ('y' != clue_reply):
                        clue_text = self.input_text(animal_text)
                        clue_reply = self.input_yes_no("The clue is: %s %s, is this OK?" % (animal_text, clue_text))

                # Now set up a new node and hook it to the 'n' response of the parent: this is the path
                # that led us to the bad guess
                #
                # This has the side-effect of removing the pointer to wrong_animal from parent_node
                new_clue = Node(clue_text,parent_node,parent_response)

                # The new animal matches the new clue
                animal_node = Node(animal_text,new_clue,'y')

                # And the wrong animal does not match the clue
                new_clue.set_child(wrong_animal,'n')

###

# Main program

guessing_game = Guessimal()
guessing_game.process_node(guessing_game.root_node)
