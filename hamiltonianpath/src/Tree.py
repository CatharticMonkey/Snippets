from Node import Node
import os

class Tree():
	def __init__(self, root = None):
		self._root = root
		self._nodeMap = dict()
		self.insertNode(root)

	def _dotConnString(self, n):
		s = ""

		for c in n.getChildren():
			s += str(n.getLabel()) + '--' + str(c.getLabel()) + ';\n'
			s += self._dotConnString(c)

		return s

	def dotString(self):
		s = "graph {\n"
		s += self._dotConnString(self.getRoot())
		s += "}"

		return s

	def writeDotToFile(self, i, j):
		dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'graphs')
		try:
			os.mkdir(dirname)
		except:
			pass

		filePath = os.path.join(dirname, 'tree' + str(j) + '.' + str(i) + '.dot')

		with open(filePath, 'w') as fp:
			fp.write(self.dotString())

	def findNewRoot(self):
		frontier = self._root.getChildren()

		while frontier:
			newFrontier = []

			for n in frontier:
				children = n.getChildren()
				if len(children) > 1:
					return n
				newFrontier += children

			frontier = newFrontier

		return self._root

	def getRoot(self):
		return self._root

	def setRoot(self, root):
		n = root
		p = n.getParent()
		root.setParent(None)

		while p:
			nextP = p.getParent()
			p.setParent(n)
			n = p
			p = nextP

		self._root = root

	def insertNode(self, n, p = None):
		n.setParent(p)
		if p:
			p.addChild(n)
		self._nodeMap[n.getLabel()] = n

	def insertNodeByLabel(self, nLabel, pLabel):
		p = self._nodeMap[pLabel]
		n = Node(nLabel, p)
		self._nodeMap[nLabel] = n
		p.addChild(n)

	def isHamiltonian(self):
		frontier = self._root.getChildren()
		if len(frontier) > 2:
			return False

		while frontier:
			newFrontier = []

			for n in frontier:
				if len(n.getChildren()) > 1:
					return False
				newFrontier += n.getChildren()

			frontier = newFrontier

		return True

	def getNodeMap(self):
		return self._nodeMap

	def getLeaves(self, currentNode = None):
		if not currentNode:
			currentNode = self._root

		numChildren = 0

		leaves = []

		for c in currentNode.getChildren():
			numChildren += 1
			leaves += self.getLeaves(c)

		if numChildren == 0:
			leaves += [currentNode]

		return leaves
