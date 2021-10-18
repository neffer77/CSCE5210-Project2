#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 20:05:35 2021

@author: bobbyfajardo
"""

''' Same as Connor's build '''
import random as rand

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
    
#similar to divisions
    
class Warehouse:
    
    def __init__(self):
        self.shelvesdictionary = {}
        self.shelves = []
        for i in range(1,64):
            self.shelves.append(node())
            self.shelves[i-1].name = str(i)
        for i in range(1,32):
            a = i*2 #even
            b = i*2+1 #odd
            self.shelves[i-1].childnodes.append(str(a))
            self.shelves[i-1].childnodes.append(str(b))
        for i in range(31,0,-1):
            
            a = i*2-1
            b = i*2
            self.shelves[a].parentnode = str(i)
            self.shelves[b].parentnode = str(i)
        self.createdictionary()
        
        #set adjacent nodes
        self.shelvesdictionary['1'].adjacentnodes = [{'name':'2', 'cost':1},{'name':'3', 'cost':1}]
        for i in range(2,64):
            self.shelvesdictionary[str(i)].adjacentnodes.append({'name':self.shelvesdictionary[str(i)].parentnode, 'cost':1})
            for j in self.shelvesdictionary[str(i)].childnodes:
                self.shelvesdictionary[str(i)].adjacentnodes.append({'name':j, 'cost':1})
    
    def createdictionary(self):  
        for i in self.shelves:
            self.shelvesdictionary[i.name]=i
            
    
    def generateChildNodes(self,currLoc):
        node = self.shelvesdictionary[currLoc]
        for i in node.adjacentnodes:
            if not i['name'] == node.parentnode:
                node.childnodes.append(self.shelvesdictionary[i['name']])
        
        
    def generateParentNodes(self,currLoc):
        node = self.shelvesdictionary[currLoc]
        for i in node.childnodes:
            i.parentnode = node.name
            
        
    def clearChildNodes(self,currLoc):
       node = self.shelvesdictionary[currLoc]
       node.childnodes.clear()
         
        
       
            
class ShelfGenerator:
    
    def __init__(self, random):
        self.random = random
        self.shelvesOrders = []
        
        
        
    def generateshelves(self):
        self.shelvesOrders = self.random.sample(range(1, 64), 3)
        self.shelvesOrders.sort() #sorted list
        
    
class WarehouseagentFunction:
    
    def __init__(self,shelvesOrders,warehouse):
        self.location = "1"
        self.shelvesOrders = shelvesOrders.shelvesOrders
        self.warehouse = warehouse
        self.cost = 0
        self.visited = []
        self.pathMem = []
        self.shelfNum = 0

#define IDS and
    
 


    def idsWarehouse(self):
        depthBound = 0
        frontier = []
        shelfgoal = False
        frontier.append({'shelfLoc':self.location, 'warehouseDepth':0})
        n = ""
        l = 0
        while not shelfgoal:
            n = frontier.pop(0)
            if n['shelfLoc'] == str(self.shelvesOrders[self.shelfNum]):
                shelfgoal = True
                self.visited.append(n['shelfLoc'])
                self.calculateWarehouseCost(shelfgoal, frontier, n, depthBound)
                return n['shelfLoc']
        
            #if self.checkWarehousepath(str(self.shelvesOrders.warehouse),n['shelfLoc']):
             #   return self.goToDest(str(self.shelvesOrders.warehouse), n['shelfLoc']) 
            
            if n['warehouseDepth'] < depthBound:
                self.warehouse.clearChildNodes(n['shelfLoc'])
                self.warehouse.generateChildNodes(n['shelfLoc'])
                self.warehouse.generateParentNodes(n['shelfLoc'])
                
                s = 0
                l = n['warehouseDepth'] + 1
                for i in self.warehouse.shelvesdictionary[n['shelfLoc']].childnodes:
                    frontier.insert(s,{'shelfLoc':i.name, 'warehouseDepth':l})
                    s = s + 1
            
            self.visited.append(n['shelfLoc'])
            self.calculateWarehouseCost(shelfgoal, frontier, n, depthBound)
            
            if len(frontier) == 0:
                frontier.append({'shelfLoc':self.location, 'warehouseDepth':0})
                depthBound = depthBound + 1
                l = 0

#define calculate cost function

    def calculateWarehouseCost(self,shelfgoal,frontier,n,depthBound):
        v = self.visited.pop(0)
        node = self.warehouse.shelvesdictionary[v]
        if node.parentnode == "":
            self.cost = self.cost + 0
        elif shelfgoal == True:
            self.cost = self.cost + 1
        else:
            #add cost to reach target shelf node
            self.cost = self.cost + 1
                        
            #add cost for going back to parent node
            if n['warehouseDepth']  == depthBound:
                self.cost = self.cost + 1
                    
            #add cost to traverse to other side of the tree
            if len(frontier) > 0 and self.warehouse.shelvesdictionary[node.parentnode].parentnode != '':
                    
                t = node
        
                while self.warehouse.shelvesdictionary[frontier[0]['shelfLoc']].parentnode != t.parentnode and self.warehouse.shelvesdictionary[frontier[0]['shelfLoc']].parentnode != t.name :            
                    t = self.warehouse.shelvesdictionary[t.parentnode]
                    self.cost = self.cost + 1
            
            #add cost to traverse back from right side of tree
            if len(frontier) == 0:
                t = node
                while self.warehouse.shelvesdictionary[t.parentnode].parentnode != '':
                    t = self.warehouse.shelvesdictionary[t.parentnode]
                    self.cost = self.cost + 1
                               
            #add cost to traverse back from a node with no children                
            if n['warehouseDepth'] != depthBound and len(self.warehouse.shelvesdictionary[node.name].childnodes) == 0:
                self.cost = self.cost + 1

    def addToWarehousePathMem(self,dest):
        shelfpath = []
        node = self.warehouse.shelvesdictionary[dest]
        shelfpath.append(node.name)
        while node.parentnode != '':
            node = self.warehouse.shelvesdictionary[node.parentnode]
            shelfpath.append(node.name)
        self.pathMem.append(shelfpath)    

    def checkWarehousepath(self, dest, currLoc):
        for i in self.pathMem:
            if currLoc in i and dest in i:
                return True
        return False
    
    def goToDest(self, dest, currLoc):
        for i in self.pathMem:
            if currLoc in i and dest in i:
                if i.index(currLoc) > i.index(dest):
                    if self.location  != currLoc:
                        for k in self.warehouse.shelvesdictionary[currLoc].adjacentnodes:
                            if k['name'] == self.warehouse.shelvesdictionary[currLoc].parentnode:
                                self.cost = self.cost + int(k['cost'])
                    for j in range(i.index(currLoc), (i.index(dest)),-1):
                        self.warehouse.shelvesdictionary[i[j-1]].parentnode = self.warehouse.shelvesdictionary[i[j]].name
                        
                        for k in self.warehouse.shelvesdictionary[i[j-1]].adjacentnodes:
                            if k['name'] == self.warehouse.shelvesdictionary[i[j-1]].parentnode:
                                self.cost = self.cost + int(k['cost'])
                    return dest
                else:
                    if self.location != currLoc:
                        for k in self.warehouse.shelvesdictionary[currLoc].adjacentnodes:
                            if k['name'] == self.warehouse.shelvesdictionary[currLoc].parentnode:
                                self.cost = self.cost + int(k['cost'])
                    
                    
                    for j in range(i.index(currLoc), (i.index(dest))):
                        
                        self.warehouse.shelvesdictionary[i[j+1]].parentnode = self.warehouse.shelvesdictionary[i[j]].name
                        for k in self.warehouse.shelvesdictionary[i[j+1]].adjacentnodes:
                            if k['name'] == self.warehouse.shelvesdictionary[i[j+1]].parentnode:
                                self.cost = self.cost + int(k['cost'])
                    return dest
        
                

'''
division names |    warehouse names
order is |          shelforder
customerOrder is |  shelvesOrders
generateDivision is | generateshelves
agentFunction is |  WarehouseagentFunction
division is |      warehouse
goal is | shelfgoal



'''


import random as rand            
def main():
    warehouse = Warehouse()   # has all properties from Warehouse class
    
    shelvesOrders = ShelfGenerator(rand)
    shelvesOrders.generateshelves()
    agent= WarehouseagentFunction(shelvesOrders, warehouse)
    print(shelvesOrders.shelvesOrders)
    #b = warehouse.shelvesdictionary['6']  #access node and 
    #print(b.name)  #prints the node name
    item = agent.idsWarehouse()
    
    
    
        
    
if __name__ == "__main__":
    main()        
        
        
        