from Node import Node

class Graph:
	def __init__(self, gDict):
		self.parseDict(gDict)

	def getNode(self, k, gDict = None):
		if k not in self._nodeMap:
			newNode = Node(k)
			self._nodeMap[k] = newNode

			for v in gDict[k]:
				newNode.addChild(self.getNode(v, gDict))

		return self._nodeMap[k]

	def parseDict(self, gDict):
		self._nodeMap = {}

		for k in gDict.keys():
			self.getNode(k, gDict)

	def getNodeMap(self):
		return self._nodeMap