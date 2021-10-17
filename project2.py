# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 14:32:54 2021

@author: conno
"""
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
        self.divisionsDict = self.addToDict()
        
        
        
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
        
    def addToDict(self):
        d = {}
        d[self.one.name] = self.one
        d[self.two.name] = self.two
        d[self.three.name] = self.three
        d[self.four.name] = self.four
        d[self.five.name] = self.five
        d[self.six.name] = self.six
        d[self.seven.name] = self.seven
        d[self.eight.name] = self.eight
        d[self.nine.name] = self.nine
        d[self.ten.name] = self.ten
        d[self.eleven.name] = self.eleven
        d[self.twelve.name] = self.twelve
        d[self.thirteen.name] = self.thirteen
        d[self.fourteen.name] = self.fourteen
        d[self.fifteen.name] = self.fifteen
        return d
        
    def generateChildNodes(self,currLoc):
        node = self.divisionsDict[currLoc]
        for i in node.adjacentnodes:
            if not i['name'] == node.parentnode:
                node.childnodes.append(self.divisionsDict[i['name']])
        
        
    def generateParentNodes(self,currLoc):
        node = self.divisionsDict[currLoc]
        for i in node.childnodes:
            i.parentnode = node.name
            
        
    def clearChildNodes(self,currLoc):
       node = self.divisionsDict[currLoc]
       node.childnodes.clear()
       
    def clearParentNodes(self,currLoc):
        node = self.divisionsDict[currLoc]
        node.parentnode = ''
            
        
class agent:
    def __init__(self,agentFunction,percept):
        self.agentFunction = agentFunction
        self.percept = percept
        
#class warehouse:
    #def __init__(self):
       
class customerOrder:
    def __init__(self,random):
        self.rand = random
        self.division = ""
        self.shelves = []
        
    def generateDivision(self):
        div = self.rand.randint(1,15)
        self.division = div
    
    def generateShelves(self):
        check = False
        while check:
            shelve = self.rand.randint(1,63)
            if shelve not in self.shelves:
                self.shelves.append(shelve)
            if len(self.shelves) == 3:
                check = True
                
    def clearDivision(self):
        self.division = ""
    
    def clearShelves(self):
        self.shelves = []
    

class agentFunction:
    
    def __init__(self,customerOrder,divisions):
        self.location = "1"
        self.customerOrder = customerOrder
        self.divisions = divisions
        self.cost = 0
        self.visited = []
        self.pathMem = []
        
    def idsDivision(self):
        depthBound = 0
        frontier = []
        goal = False
        frontier.append({'loc':self.location, 'depth':0})
        n = ""
        l = 0 
        while not goal:
            n = frontier.pop(0)
            if n['loc'] == str(self.customerOrder.division):
                goal = True
                self.visited.append(n['loc'])
                self.calculateCost(goal, frontier,n,depthBound)
                return n

                
            if n['depth'] < depthBound:
                self.divisions.clearChildNodes(n['loc'])
                self.divisions.generateChildNodes(n['loc'])
                self.divisions.generateParentNodes(n['loc'])
                s = 0
                l = n['depth'] + 1
                for i in self.divisions.divisionsDict[n['loc']].childnodes:
                    frontier.insert(s,{'loc':i.name, 'depth':l})
                    s = s + 1
                    
            self.visited.append(n['loc'])
            self.calculateCost(goal, frontier,n,depthBound)
            
            if len(frontier) == 0:
                frontier.append({'loc':self.location, 'depth':0})
                depthBound = depthBound + 1
                l = 0
    
    #counted forward and backward and combined
    def calculateCost(self,goal,frontier,n,depthBound):
        for i in self.visited:
            v = self.visited.pop(0)
            node = self.divisions.divisionsDict[v]
            if node.parentnode == "":
                self.cost = self.cost + 0
            elif goal == True:
                for i in self.divisions.divisionsDict[node.name].adjacentnodes:
                    if i['name'] == node.parentnode:
                        self.cost = self.cost + int(i['cost'])
            else:
                #add cost to reach node
                for i in self.divisions.divisionsDict[node.name].adjacentnodes:
                    if i['name'] == node.parentnode:
                        self.cost = self.cost + int(i['cost'])
                
                #add cost to go back to parent node
                if n['depth'] == depthBound:
                    for i in self.divisions.divisionsDict[node.name].adjacentnodes:
                        if i['name'] == node.parentnode:
                            self.cost = self.cost + int(i['cost'])
        
                #add cost to traverse to other side of the tree    
                if len(frontier) > 0 and self.divisions.divisionsDict[node.parentnode].parentnode != '':
                        #print (node.name)
                        t = node
                        while self.divisions.divisionsDict[frontier[0]['loc']].parentnode != t.parentnode and self.divisions.divisionsDict[frontier[0]['loc']].parentnode != t.name :
                                t = self.divisions.divisionsDict[t.parentnode]
                                for i in self.divisions.divisionsDict[t.name].adjacentnodes:
                                    if i['name'] == t.parentnode:
                                        self.cost = self.cost + int(i['cost'])
                if len(frontier) == 0:
                    t = node
                    while self.divisions.divisionsDict[t.parentnode].parentnode != '':
                        t = self.divisions.divisionsDict[t.parentnode]
                        for i in self.divisions.divisionsDict[t.name].adjacentnodes:
                            if i['name'] == t.parentnode:
                                self.cost = self.cost + int(i['cost'])
   
         
    def addToPathMem(self,dest):
        path = []
        node = self.divisions.divisionsDict[dest['loc']]
        path.append(node.name)
        while node.parentnode != '':
            node = self.divisions.divisionsDict[node.parentnode]
            path.append(node.name)
        self.pathMem.append(path)
              
            
        
#class percept:
 #   def __init__(self):

def main():
   order = customerOrder(rand)
   order.generateDivision()
   
   division = divisions()
   af = agentFunction(order, division)
   
   goal = af.idsDivision()
   af.addToPathMem(goal)
   print(af.pathMem)
   print (goal)
   print (af.cost)
   
   order.generateDivision()
   af.location = goal['loc']
   af.cost = 0
   division.clearParentNodes(af.location)
   goal = af.idsDivision()
   af.addToPathMem(goal)
   print(af.pathMem)
   print (goal)
   print (af.cost)
   
    
if __name__ == "__main__":
    main()
    
    