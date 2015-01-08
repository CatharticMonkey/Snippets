from SampleGraphs import graphs
from Tree import Tree
from Node import Node
from Graph import Graph

def selectInitialTree(g):
	nodeMap = g.getNodeMap()
	treeCandidates = dict()

	for n in nodeMap.keys():
		tree = shallowSpanningTree(nodeMap[n])
		height = tree.getRoot().getSubtreeHeight()
		rootChildren = len(tree.getRoot().getChildren())

		if rootChildren > 1:
			if not rootChildren in treeCandidates:
				treeCandidates[rootChildren] = dict()

			if not height in treeCandidates[rootChildren]:
				treeCandidates[rootChildren][height] = []

			treeCandidates[rootChildren][height] += [tree]

	minChildren = min(treeCandidates.keys())
	minHeight = min(treeCandidates[minChildren].keys())

	return treeCandidates[minChildren][minHeight][0]

def shallowSpanningTree(root):
	visited = [root.getLabel()]
	retTree = Tree(Node(root.getLabel()))
	frontier = [root]

	while frontier:
		newFrontier = []

		for n in frontier:
			nLabel = n.getLabel()
			for c in n.getChildren():
				cLabel = c.getLabel()
				if cLabel not in visited:
					visited += [cLabel]
					retTree.insertNodeByLabel(cLabel, nLabel)
					newFrontier += [c]

		frontier = newFrontier

	return retTree

def getPossibleSwitches(tree, origGraph):
	possibleBranchRemovingSwitches = dict()
	possibleNonBranchRemovingSwitches = dict()
	root = tree.getRoot()
	visited = []
	frontier = [root]
	leaves = set([n.getLabel() for n in set(tree.getLeaves())])

	while frontier:
		newFrontier = []

		for n in frontier:
			nLabel = n.getLabel()
			visited += [nLabel]
			origN = origGraph.getNode(nLabel)

			possibleParents = set([c.getLabel() for c in origN.getChildren()]).intersection(leaves)
			descendents = set([d.getLabel() for d in n.getDescendents()])
			possibleParents -= descendents

			for pLabel in possibleParents:
				p = tree.getNodeMap()[pLabel]
				newHeight = p.getLevel() + n.getSubtreeHeight()

				if len(n.getParent().getChildren()) > 1:
					possibleSwitches = possibleBranchRemovingSwitches
				else:
					possibleSwitches = possibleNonBranchRemovingSwitches

				if not newHeight in possibleSwitches:
					possibleSwitches[newHeight] = []

				possibleSwitches[newHeight] += [(n, p)]

			newFrontier += n.getChildren()

		frontier = newFrontier

	if len(possibleBranchRemovingSwitches.keys()) > 0:
		return possibleBranchRemovingSwitches
	else:
		return possibleNonBranchRemovingSwitches

j = 0

for graph in graphs:
	g = Graph(graph)
	tree = selectInitialTree(g)
	tree.writeDotToFile(0, j)

	for i in range(1, 20):
		if tree.isHamiltonian():
			break

		possibleSwitches = getPossibleSwitches(tree, g)
		if possibleSwitches.keys():
			shortestNewPath = min(possibleSwitches.keys())
			node, parent = possibleSwitches[shortestNewPath][0]
			node.setParent(parent)
		elif len(tree.getRoot().getChildren()) == 1:
			newRoot = tree.findNewRoot()
			tree.setRoot(newRoot)
		else:
			break

		tree.writeDotToFile(i, j)

	print "Tree " + str(j) + " is hamiltonian? " + str(tree.isHamiltonian())

	j += 1