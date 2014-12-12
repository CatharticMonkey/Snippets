import copy

graph = {
	'A' : ['B', 'C', 'E'],
	'B' : ['A', 'D'],
	'C' : ['A', 'D'],
	'D' : ['B', 'C', 'E'],
	'E' : ['A', 'D']
}

graph = {
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
}

graph = {
	1 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	2 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	3 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	4 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	5 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	6 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	7 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	8 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	9 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	10 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	11 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

for n in graph.keys():
	graph[n].remove(n)




graph = {
	1 : [2],
	2 : [1, 3, 4],
	3 : [2, 4, 7],
	4 : [2, 3, 5],
	5 : [4, 6, 7],
	6 : [5],
	7 : [3, 5]
}

graph = {
	1 : [2],
	2 : [1, 3, 5],
	3 : [2, 4, 9],
	4 : [3, 5],
	5 : [2, 4, 6],
	6 : [5, 7, 8],
	7 : [6],
	8 : [6, 9],
	9 : [3, 8]
}

cutGraph = copy.deepcopy(graph)

def removeEdge(g, nodeA, nodeB):
	if nodeA in g:
		g[nodeA].remove(nodeB)

	if nodeB in g:
		g[nodeB].remove(nodeA)

def cullToMinConnected(g, currentNode, visitedNodes = set(), keptEdges = set()):
	nextNodes = set(g[currentNode])
	removalNodes = nextNodes.intersection(visitedNodes)

	for n in removalNodes:
		if (n, currentNode) not in keptEdges:
			removeEdge(g, currentNode, n)

	unVisitedNodes = nextNodes.difference(visitedNodes)

	visitedNodes.add(currentNode)
	visitedNodes.update(unVisitedNodes)

	for n in unVisitedNodes:
		keptEdges.add((currentNode, n))

	for n in unVisitedNodes:
		cullToMinConnected(g, n, visitedNodes, keptEdges)

def findCurrentEnds(g):
	return [n for n in g.keys() if len(g[n]) == 1]

def getDegreeOfPointsConnectedToEnds(g):
	return {n: len(g[g[n][0]]) for n in findCurrentEnds(g)}

def getPairsOfEndPointsSharingNeighbours(g):
	ends = findCurrentEnds(g)
	retList = []

	for i in range(len(ends)):
		n = ends[i]
		for j in range(i, len(ends)):
			m = ends[j]
			if n != m and len(set(g[n]).intersection(g[m])) == 1:
				retList += [(n, m)]

	return retList

def getPairsOfEndPoints(g):
	ends = findCurrentEnds(g)
	retList = []

	for i in range(len(ends)):
		n = ends[i]
		for j in range(i, len(ends)):
			m = ends[j]
			if n != m:
				retList += [(n, m)]

	return retList

def getPathIfHamiltonian(g):
	ends = findCurrentEnds(g)
	if len(ends) > 2:
		return False

	start = ends[0]
	current = start
	visited = [start]

	while current != ends[1]:
		nextNode = [n for n in g[current] if n not in visited]
		if len(nextNode) == 0:
			return None
		current = nextNode[0]
		visited += [current]

	return visited

#TODO: Find all loops which can be obtained by adding one edge from origG to g
def findPotentialLoopsWithCurrentPath(currentNode, g, origG, visitedNodes = []):
	retList = []

	visitedNodes += [currentNode]

	for n in set(origG[currentNode]).difference(set(g[currentNode])):
		if n in visitedNodes and n != currentNode:
			loopNodes = visitedNodes[visitedNodes.index(n):]
			loopExits = [x for x in loopNodes if len(set(origG[x]).difference(set(loopNodes))) > 0]
			retList += [(n, currentNode, copy.deepcopy(visitedNodes), loopExits)]

	for n in g[currentNode]:
		if n not in visitedNodes:
			subVisitedNodes = copy.deepcopy(visitedNodes)
			retList += findPotentialLoopsWithCurrentPath(n, g, origG, subVisitedNodes)

	return retList

def isSublist(sl, l):
	sublistFound = False

	for i in range(len(l)):
		for j in range(len(sl)):
			sublistFound = sublistFound and not l[(i + j) % len(l)] != sl[j]
			if not sublistFound:
				break

		if sublistFound:
			break

	return sublistFound

def rearrangeWithCycles(g, origG):
	cycles = [1]
	while len(cycles) > 0:
		cycles = findPotentialLoopsWithCurrentPath(g.keys()[0], g, origG)
		ends = findCurrentEnds(g)
		for c in cycles:
			print c
			start, end, nodes, ioNodes = c
			cycleEndsConnectingToEnds = {m : n for m in ioNodes for n in origG[m] if n in ends and n not in g[m]}
			startIndex = nodes.index(start)
			endIndex = nodes.index(end)

			for n in cycleEndsConnectingToEnds.keys():
				index = nodes.index(n)
				m = cycleEndsConnectingToEnds[n]
				#TODO: This is wrong. Should be based on entry and exit nodes from a loop
				#	So we want to find an exit node (connecting to an endpoint)
				#	which is next to another exit node?
				if (index == startIndex + 1 and m not in nodes) or (index == endIndex - 1 and m in nodes):
					g[start] += [end]
					g[end] += [start]
					if n in g[start]:
						g[start].remove(n)
					elif n in g[end]:
						g[end].remove(n)
					g[n] += [m]
					g[m] += [n]

					break

def tryMatchEndPoints(g, origG):
	pairs = getPairsOfEndPoints(g)
	degrees = getDegreeOfPointsConnectedToEnds(g)
	for n, m in pairs:
		if m in origG[n] and degrees[n] > 2:
			g[g[n][0]].remove(n)
			g[n] = [m]
			g[m] += [n]
			return True
		elif n in origG[m] and degrees[m] > 2:
			g[g[m][0]].remove(m)
			g[m] = [n]
			g[n] += [m]
			return True

	return False

cullToMinConnected(cutGraph, graph.keys()[0])

done = False

while not done:
	done = not tryMatchEndPoints(cutGraph, graph)
	rearrangeWithCycles(cutGraph, graph)

outPath = getPathIfHamiltonian(cutGraph)
if outPath:
	print outPath
else:
	print "Not hamiltonian"
	print cutGraph
