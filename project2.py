# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 14:32:54 2021

@author: conno
"""

class node:
    
    def __init__(self):
        self.name = ""
        self.parentnode = ""
        self.childnodes = []
        self.adjacentnodes = []
        
    def setName(self,n):
        self.name = n
        
    def getName(self):
        return self.name
        
    def setParentNode(self,parent):
        self.parentnode = parent
        
    def getParentNode(self):
        return self.parentnode
    
    def setChildNodes(self,children):
        self.childnodes = children
    
    def getChildNodes(self):
        return self.childnodes
    
    def setAdjacentNodes(self,adjNodes):
        self.adjacentnodes = adjNodes
        
    def getAdjacentNodes(self):
        return self.adjacentnodes
    
    
class divisions:
    
    def __init__(self):
        self.one = node()
        self.two = node()
        self.three = node()
        self.four = node()
        self.five = node()
        self.six = node()
        self.seven = node()
        self.eight = node()
        self.nine = node()
        self.ten = node()
        self.eleven = node()
        self.twelve = node()
        self.thirteen = node()
        self.fourteen = node()
        self.fifteen = node()
        self.addNames()
        self.addAdjacents()
        
        
        
    def addNames(self):
        self.one.setName("1")
        self.two.setName("2")
        self.three.setName("3")
        self.four.setName("4")
        self.five.setName("5")
        self.six.setName("6")
        self.seven.setName("7")
        self.eight.setName("8")
        self.nine.setName("9")
        self.ten.setName("10")
        self.eleven.setName("11")
        self.twelve.setName("12")
        self.thirteen.setName("13")
        self.fourteen.setName("14")
        self.fifteen.setName("15")
        
    def addAdjacents(self):
        self.one.setAdjacentNodes([{'name':'2', 'cost':20},{'name':'3', 'cost':20}])
        self.two.setAdjacentNodes([{'name':'4', 'cost':20},{'name':'5', 'cost':30},{'name':'1', 'cost':20}])
        self.three.setAdjacentNodes([{'name':'6', 'cost':40},{'name':'7', 'cost':10},{'name':'1', 'cost':20}])
        self.four.setAdjacentNodes([{'name':'2', 'cost':20},{'name':'8', 'cost':10},{'name':'9', 'cost':20}])
        self.five.setAdjacentNodes([{'name':'2', 'cost':30},{'name':'10', 'cost':30},{'name':'11', 'cost':20}])
        self.six.setAdjacentNodes([{'name':'3', 'cost':40},{'name':'12', 'cost':30},{'name':'13', 'cost':20}])
        self.seven.setAdjacentNodes([{'name':'3', 'cost':10},{'name':'14', 'cost':20},{'name':'15', 'cost':20}])
        self.eight.setAdjacentNodes([{'name':'4', 'cost':10}])
        self.nine.setAdjacentNodes([{'name':'4', 'cost':20}])
        self.ten.setAdjacentNodes([{'name':'5', 'cost':30}])
        self.eleven.setAdjacentNodes([{'name':'5', 'cost':20}])
        self.twelve.setAdjacentNodes([{'name':'6', 'cost':30}])
        self.thirteen.setAdjacentNodes([{'name':'6', 'cost':20}])
        self.fourteen.setAdjacentNodes([{'name':'7', 'cost':20}])
        self.fifteen.setAdjacentNodes([{'name':'7', 'cost':20}])

class agent:
    def __init__(self,agentFunction,percept):
        self.location = "1"
        self.agentFunction = agentFunction
        self.percept = percept
        
class warehouse:
    def __init__(self):
    
class agentFunction:
    def __init__(self):
        
class percept:
    def __init__(self):

def main():
    a = node()
    
    
if __name__ == "__main__":
    main()
    
    