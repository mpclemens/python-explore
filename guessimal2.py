#!/usr/bin/env python

import pickle # to serialize/unserialize the data file

# Class to represent a binary tree of clues with leaf nodes representing
# animals
#
class Node:

	# set up a new node, possibly hanging it from a parent node
	# when given a certain answer ("y" or "n", for example)
	def __init__(self,my_text,parent_node=None,parent_answer=None):
		self.text = my_text
		self.children = {}
		if (None != parent_node and None != parent_answer):
			parent_node.set_child(self,parent_answer)

	# true if this is a leaf node
	#
	def is_leaf(self):
		return(None == self.children or 0 == len(self.children.keys()))

	# hook a new node under the current node, pointed to by an 
	# answer provided by the user
	def set_child(self,child_node,my_answer):
		self.children[my_answer] = child_node

	# return the child node hooked to an answer, if any
	def get_child(self,my_answer):
		if (None == self.children or my_answer not in self.children):
			return(None)
		else:
			return(self.children[my_answer])


	# make a small (and boring!) tree of animals, returning the root
	#
	@classmethod
	def init_tree(class_name):
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


	# load a tree from the given file, or initialize it to a default tree
	@classmethod
	def load_tree(class_name,file_name):
		if (None != file_name):
			# Try loading from the supplied file
			try:
				data_file = open(file_name)
				root_node = pickle.load(data_file)
			except IOError:
				# bad things happened, so just return the default tree
				root_node = Node.init_tree()
		else:
			root_node = Node.init_tree()
		return root_node

	# archive the tree for future games
	def save_tree(self,file_name):
		try:
			data_file = open(file_name,"w")
			pickle.dump(self, data_file)
		except IOError as e:
			print "ERROR: could not save data file"
			raise e

# Class to handle the game mechanics: prompting the user and processing the input

class Guessimal:

	# Start a new game, loading from a previous save, if any
	def __init__(self,file_name="guessimal2.data"):
		self.root_node = Node.load_tree(file_name)

	def input_yes_no(self,prompt_text):
		user_input = raw_input(prompt_text + " (Y/N) ")
		# first character, lower-cased to make comparison easier
		user_input = user_input.lstrip().lower()
		return user_input[0]

	def input_text(self,prompt_text):
		user_input = raw_input(prompt_text)

		# lop off leading and trailing whitespace
		user_input = user_input.lstrip().rstrip()
		return user_input	


	# Handle each node appropriately: leaves are animals, others are clues
	def process_node(self,current_node):
		if (current_node.is_leaf()):
			# Found an animal...
			user_response = self.input_yes_no("Is your animal " + current_node.text + "?")
			# but if it's the wrong one, then the tree gets extended
			if ('n' == user_response):
				self.add_clue(self.previous_clue, self.previous_response, current_node)
				print "Thanks! Now I'm going to save the clues for next time"
				self.root_node.save_tree("guessimal.data")
			else:
				print "I am very clever!"
				
		else:
			# Found a clue, so ask it and recurse into the subtree
			self.previous_clue = current_node # needed when we add an animal (parent of new leaf node)

			user_response = self.input_yes_no("Your animal " + current_node.text + "?")
			self.previous_response = user_response

			self.process_node(current_node.get_child(user_response))

	# The user is too clever! Add a new clue and animal in the tree that differentiates it from the
	# bad guess
	def add_clue(self, parent_node, parent_response, wrong_animal):
		print "OK, you stumped me. Tell me the animal you were thinking of so I can learn it."
		print "Be sure to add \"a\" or \"an\" in front of the name, like \"a giraffe\"."

		animal_reply = 'n'
		while ('y' != animal_reply):
			animal_text = self.input_text("Your animal is: ")
			animal_reply = self.input_yes_no("Your animal is " + animal_text + ", is this OK?")
		

		print "Now I need to know what makes " + animal_text + " different from " + wrong_animal.text + "."
		print "Please write a clue that finishes this sentence... "

		clue_reply = 'n'
		while ('y' != clue_reply):
			clue_text = self.input_text(animal_text + "... ")
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

# Main body of the program

guessing_game = Guessimal()
guessing_game.process_node(guessing_game.root_node)
