import floor 

class CellNode:
    def __init__(self,Cell):
        self.referenceTo = Cell
        self.parrent = None
        self.listOfChildren = []
        self.pathCostFromRoot = 0
        
    def addChild(self,childNode):
        self.listOfChildren.append(childNode)

    def setParrent(self,parrent):
        self.parrent = parrent

    def getParrent(self):
        return self.parrent
    
    def getCell(self):
        return self.referenceTo
    
    def getPathCostFromRoot(self):
        return self.pathCostFromRoot
    
    def setPathCostFromRoot(self,pathCostFromRoot):
        self.pathCostFromRoot = pathCostFromRoot

