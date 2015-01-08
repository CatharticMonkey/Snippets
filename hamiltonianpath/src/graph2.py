graphs = [{
	'A' : ['B', 'C', 'E'],
	'B' : ['A', 'D'],
	'C' : ['A', 'D'],
	'D' : ['B', 'C', 'E'],
	'E' : ['A', 'D']
},
{
	1 : [2, 4, 6],
	2 : [1, 3, 5, 7],
	3 : [6, 8, 2],
	4 : [1, 9, 5],
	5 : [2, 4, 10],
	6 : [1, 3, 9, 11],
	7 : [2, 10, 8],
	8 : [3, 7, 11],
	9 : [4, 6, 10],
	10 : [5, 7, 9, 11],
	11 : [6, 8, 10]
},
{
	1 : [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	2 : [1, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	3 : [1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
	4 : [1, 2, 3, 5, 6, 7, 8, 9, 10, 11],
	5 : [1, 2, 3, 4, 6, 7, 8, 9, 10, 11],
	6 : [1, 2, 3, 4, 5, 7, 8, 9, 10, 11],
	7 : [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
	8 : [1, 2, 3, 4, 5, 6, 7, 9, 10, 11],
	9 : [1, 2, 3, 4, 5, 6, 7, 8, 10, 11],
	10 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 11],
	11 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
},
{
	1 : [2],
	2 : [1, 3, 4],
	3 : [2, 4, 7],
	4 : [2, 3, 5],
	5 : [4, 6, 7],
	6 : [5],
	7 : [3, 5]
},
{
	1 : [2],
	2 : [1, 3, 5],
	3 : [2, 4, 9],
	4 : [3, 5],
	5 : [2, 4, 6],
	6 : [5, 7, 8],
	7 : [6],
	8 : [6, 9],
	9 : [3, 8]
}]

class Graph:
	def __init__(self, rootNode, graphDict, depthDict):
		self._root = rootNode
		self._graphDict = graphDict
		self._depthDict = depthDict

	def getRoot(self):
		return self._root

	def getGraphDict(self):
		return self._graphDict

	def getDepthDict(self):
		return self._depthDict

	def setRoot(self, newRoot):
		self._root = newRoot

def makeShallowTree(g, rootNode):
	retG = Graph(rootNode, {}, {})
	depth = 0
	graphDict = retG.getGraphDict()
	depthDict = retG.getDepthDict()
	visitedNodes = [rootNode]
	frontier = [rootNode]

	while frontier:
		newFrontier = []
		depthDict[depth] = []

		for n in frontier:
			graphDict[n] = []
			depthDict[depth] += [n]

			for c in g[n]:
				if c not in visitedNodes:
					graphDict[n] += [c]
					visitedNodes += [c]
					newFrontier += [c]

		frontier = newFrontier

		depth += 1

	return retG

def resetGraphDepths(g):
	depthDict = g.getDepthDict()
	graphDict = g.getGraphDict()
	frontier = [g.getRoot()]
	depth = 0

	while frontier:
		newFrontier = []
		depthDict[depth] = []
		for n in frontier:
			depthDict[depth] += [n]
			for c in graphDict[n]:
				newFrontier += [c]

		frontier = newFrontier

		depth += 1

def dotString(g):
	s = "graph {\n"
	for k in g.keys():
		for j in g[k]:
			s += str(k) + '--' + str(j) + ';\n'
	s += "}"

	return s

def subTreeHeight(g, root):
	maxTreeHeight = 0
	for n in g.getGraphDict()[root]:
		maxTreeHeight = max(maxTreeHeight, subTreeHeight(g, n))

	return maxTreeHeight

def rearrange(g, origG):
	depthDict = g.getDepthDict()
	leaves = getLeaves(g)
	root = g.getRoot()

	maxLength = 0
	topNodeSwitch = [None, None]

	for d in depthDict.keys():
		for n in depthDict[d]:
			for l in leaves:
				if n in origG[l] and l not in getDescendents(g, n):
					currLen = getNodeDepth(depthDict, l) + subTreeHeight(g, n)
					if currLen > maxLength:
						topNodeSwitch = [n, l]
						maxLength = currLen

		if maxLength > 0:
			break

	if maxLength > 0:
		n = topNodeSwitch[0]
		l = topNodeSwitch[1]
		p = getParent(g, n)
		g.getGraphDict()[p].remove(n)
		g.getGraphDict()[l] += [n]
		resetGraphDepths(g)
		return True
	else:
		ret = recursiveSetNewRoot(pickNewHighRoot(g), g, root, [root])
		if ret:
			resetGraphDepths(g)
		else:
			ret = recursiveSetNewRoot(pickNewDeepRoot(g), g, root, [root])
			resetGraphDepths(g)
		return ret

def pickNewHighRoot(g):
	depthDict = g.getDepthDict()
	graphDict = g.getGraphDict()

	for d in depthDict.keys():
		for n in depthDict[d]:
			if len(graphDict[n]) > 1:
				return n

def pickNewDeepRoot(g):
	depthDict = g.getDepthDict()
	graphDict = g.getGraphDict()

	for d in depthDict.keys():
		for n in depthDict[d]:
			if len(graphDict[n]) > 1:
				newRoot = n

	return newRoot

def getLeaves(gClass):
	g = gClass.getGraphDict()
	return [n for n in g.keys() if not g[n]]

def getDescendents(g, r):
	descendents = [r]
	frontier = [r]

	while frontier:
		newFrontier = []
		for n in frontier:
			descendents += [n]
			newFrontier += g.getGraphDict()[n]

		frontier = newFrontier

	return descendents

def getParent(gClass, n):
	g = gClass.getGraphDict()
	for p in g.keys():
		if n in g[p]:
			return p

def getNodeDepth(gDepth, n):
	for d in gDepth.keys():
		if n in gDepth[d]:
			return d

def recursiveSetNewRoot(newRoot, g, currentNode, currentPath):
	if g.getRoot() == newRoot:
		return False

	if currentNode == newRoot:
		d = g.getGraphDict()
		d[currentNode] += [g.getRoot()]

		for i in range(len(currentPath)):
			n = currentPath[i]
			d[n] = [item for item in d[n] if item not in currentPath and item != currentNode]
			if i > 0:
				d[n] += [currentPath[i - 1]]

		g.setRoot(newRoot)

	else:
		for n in g.getGraphDict()[currentNode]:
			recursiveSetNewRoot(newRoot, g, n, currentPath + [n])

		if g.getRoot() != newRoot:
			return False

	return True

# A tree is hamiltonian if the root has no more than two children and every
# other node has only one child.
def isHamiltonian(g):
	d = g.getGraphDict()
	for k in d.keys():
		if len(d[k]) > 2 or (len(d[k]) > 1 and k != g.getRoot()):
			return False

	return True

for j in range(len(graphs)):
	graph = graphs[j]
	root = graph.keys()[0]
	for k in graph.keys():
		if len(graph[k]) > 1:
			root = k

	i = 0

	i += 1
	with open('tree' + str(j) + '.' + str(i) + '.dot', 'w') as fp:
		fp.write(dotString(graph))

	treeGraph = makeShallowTree(graph, root)

	i += 1
	with open('tree' + str(j) + '.' + str(i) + '.dot', 'w') as fp:
		fp.write(dotString(treeGraph.getGraphDict()))

	while rearrange(treeGraph, graph):
		i += 1
		with open('tree' + str(j) + '.' + str(i) + '.dot', 'w') as fp:
			fp.write(dotString(treeGraph.getGraphDict()))

		isHam = isHamiltonian(treeGraph)

		if i > len(graph.keys()) * len(graph.keys()) or isHam:
			break

	print 'Is hamiltonian: ' + str(isHam)