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
    
def main():
    a = node()
    
    
if __name__ == "__main__":
    main()
    
    