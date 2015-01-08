class Node:
	def __init__(self, label, parent = None):
		self._label = label
		self._parent = parent
		self._children = set()

	def getLabel(self):
		return self._label

	def getParent(self):
		return self._parent

	def getChildren(self):
		return self._children

	def removeChild(self, child):
		self._children.remove(child)

	def addChild(self, child):
		self._children.add(child)

	def setParent(self, newParent):
		if self._parent:
			self._parent.removeChild(self)
		if newParent:
			newParent.addChild(self)
		self._parent = newParent

	def getDescendents(self):
		descendents = []
		for c in self._children:
			descendents += c.getDescendents()

		descendents += self._children
		return set(descendents)

	def getLevel(self):
		if self._parent:
			return self._parent.getLevel() + 1
		else:
			return 0

	def getSubtreeHeight(self):
		maxHeight = 1

		for c in self._children:
			maxHeight = max(maxHeight, c.getSubtreeHeight()) + 1

		return maxHeight