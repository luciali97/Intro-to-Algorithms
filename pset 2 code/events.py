# The Event class does not need to be modified.
class Event(object):
	def __init__(self, time, description = ""):
		self.time = time
		self.description = description

	# Consider two events to be equal if they have the same .time and .description.
	def __eq__(self, other):
	    if isinstance(other, self.__class__):
	        return self.__dict__ == other.__dict__
	    return NotImplemented

	def __ne__(self, other):
	    if isinstance(other, self.__class__):
	        return not self.__eq__(other)
	    return NotImplemented

# This is the data structure you should improve.
class Timeline(object):
	def __init__(self):
		self.evts = AVLTree()

	def add_event(self, event):
		self.evts.insert(event.time,event.description)

	def events_in_range(self, start, end):
		# Currently, the runtime of this operation is O(n). Your goal is O(k + log n).
		elist = []
		e = self.evts.find(start)
		while e != None and e.key <= end:
			 elist.append(Event(e.key,e.value))
			 e = e.successor
		# def inorder_walk(e):
		# 	if e == None:
		# 		return
		# 	if e.left != None and e.key > start: 
		# 		inorder_walk(e.left)
		# 	if e.key >=start and e.key <= end:
		# 		elist.append(Event(e.key,e.value))
		# 	if e.right != None and e.key < end: 
		# 		inorder_walk(e.right)
		# 	return
		# inorder_walk(self.evts.root)
		return elist
		#return [e for e in self.events if start <= e.time <= end]

# Below is a partial implementation of AVl trees. Note in particular that find is not implemented.
class AVLNode(object):
	def __init__(self, key, value, parent = None, left = None, right = None):
		self.key = key
		self.value = value
		self.parent = parent
		self.left = left
		self.right = right
		self.update_height()
		self.update_successor()

	def right_subtree_height(self):
		if self.right is not None:
			return self.right.height
		return 0

	def left_subtree_height(self):
		if self.left is not None:
			return self.left.height
		return 0

	def update_height(self):
		# Shallow-- assumes left and right children have correct .height.
		# Leaves have height 1.
		self.height = max(self.left_subtree_height(), self.right_subtree_height()) + 1

	def balance_factor(self):
		return self.right_subtree_height() - self.left_subtree_height()

	def find_min(self):
		x = self
		while x.left != None:
			x = x.left
		return x

	def update_successor(self):
		if self.right != None:
			self.successor = self.right.find_min()
		x = self
		while x.parent != None and x == x.parent.right:
			x = x.parent
		self.successor = x.parent
		if self.left == None:
			y = self
			while y.parent != None and y == y.parent.left:
				y = y.parent
			if y.parent != None:
				y.parent.successor = self

class AVLTree(object):
	def __init__(self):
		self.root = None  # indicates the tree is empty

	""" 
		Returns the node with the smallest .key greater than or equal to key.
	""" 
	def find(self, key):
		x = self.root
		smallest = x
		while x != None:
		 	if x.key < key:
		 		x = x.right
		 	else:
		 		smallest = x
		 		x = x.left
		return smallest
		raise NotImplementedError()

	def rotate_left(self, node):
		# This should only be called on a node whose right subtree is not empty.
		x = node
		y = node.right
		B = y.left

		# Move y up.
		if node.parent:
			if node.parent.left == node:
				node.parent.left = y
			elif node.parent.right == node:
				node.parent.right = y
			y.parent = node.parent
		else:
			self.root = y
			y.parent = None

		# Move x down.
		y.left = x
		x.parent = y

		# Rearrange children.
		x.right = B
		if B:
			B.parent = x

		x.update_height()
		y.update_height()

	def rotate_right(self, node):
		# This should only be called on a node whose left subtree is not empty.
		y = node
		x = node.left
		B = x.right
		if node.parent:
			if node.parent.left == node:
				node.parent.left = x
			elif node.parent.right == node:
				node.parent.right = x
			x.parent = node.parent
		else:
			self.root = x
			x.parent = None

		x.right = y
		y.parent = x

		y.left = B
		if B:
			B.parent = y

		x.update_height()
		y.update_height()

	def insert(self, key, value):
		if not self.root:
			self.root = AVLNode(key, value)
			return

		current = self.root
		while True:
			if key <= current.key:
				if current.left is None:
					current.left = AVLNode(key, value, current)
					break
				else:
					current = current.left
			else:
				if current.right is None:
					current.right = AVLNode(key, value, current)
					break
				else:
					current = current.right

		# Now backtrack along ancestors, rotating as necessary.
		while current is not None:
			current.update_height()  # because we inserted a node
			if current.balance_factor() > 1:
				if current.right.balance_factor() >= 0:
					self.rotate_left(current)
				else:
					self.rotate_right(current.right)
					self.rotate_left(current)
			elif current.balance_factor() < -1:
				if current.left.balance_factor() <= 0:
					self.rotate_right(current)
				else:
					self.rotate_left(current.left)
					self.rotate_right(current)
			current = current.parent