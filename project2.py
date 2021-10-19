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
        shelves = rand.sample(range(1, 64), 3)
        self.shelvesOrders = shelves
        self.shelvesOrders.sort() #sorted list
        
    
class WarehouseagentFunction:
    
    def __init__(self,shelvesOrders,warehouse):
        self.location = "1"
        self.shelvesOrders = shelvesOrders
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
            if n['shelfLoc'] == str(self.shelvesOrders.shelvesOrders[self.shelfNum]):
                shelfgoal = True
                self.visited.insert(0,n['shelfLoc'])
                self.calculateWarehouseCost(shelfgoal, frontier, n, depthBound)
                return n['shelfLoc']
        
            if self.checkWarehousepath(str(self.shelvesOrders.shelvesOrders[self.shelfNum]),n['shelfLoc']):
                self.visited.insert(0,n['shelfLoc'])
                return self.goToDest(str(self.shelvesOrders.shelvesOrders[self.shelfNum]), n['shelfLoc']) 
            
            if n['warehouseDepth'] < depthBound:
                self.warehouse.clearChildNodes(n['shelfLoc'])
                self.warehouse.generateChildNodes(n['shelfLoc'])
                self.warehouse.generateParentNodes(n['shelfLoc'])
                
                s = 0
                l = n['warehouseDepth'] + 1
                for i in self.warehouse.shelvesdictionary[n['shelfLoc']].childnodes:
                    frontier.insert(s,{'shelfLoc':i.name, 'warehouseDepth':l})
                    s = s + 1
            
            self.visited.insert(0, n['shelfLoc'])
            self.calculateWarehouseCost(shelfgoal, frontier, n, depthBound)
            
            if len(frontier) == 0:
                frontier.append({'shelfLoc':self.location, 'warehouseDepth':0})
                depthBound = depthBound + 1
                l = 0

#define calculate cost function

    def calculateWarehouseCost(self,shelfgoal,frontier,n,depthBound):
        v = self.visited.pop(0)
        self.visited.insert(0, v)
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
                self.visited.insert(0, node.parentnode)    
            #add cost to traverse to other side of the tree
            if len(frontier) > 0 and self.warehouse.shelvesdictionary[node.parentnode].parentnode != '':
                    
                t = node
        
                while self.warehouse.shelvesdictionary[frontier[0]['shelfLoc']].parentnode != t.parentnode and self.warehouse.shelvesdictionary[frontier[0]['shelfLoc']].parentnode != t.name :            
                    t = self.warehouse.shelvesdictionary[t.parentnode]
                    self.cost = self.cost + 1
                    self.visited.insert(0, t.parentnode)
            #add cost to traverse back from right side of tree
            if len(frontier) == 0:
                t = node
                while self.warehouse.shelvesdictionary[t.parentnode].parentnode != '':
                    t = self.warehouse.shelvesdictionary[t.parentnode]
                    self.cost = self.cost + 1
                    self.visited.insert(0, t.parentnode)           
            #add cost to traverse back from a node with no children                
            if n['warehouseDepth'] != depthBound and len(self.warehouse.shelvesdictionary[node.name].childnodes) == 0:
                self.cost = self.cost + 1
                self.visited.insert(0, node.parentnode)

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
                        self.cost = self.cost + 1
                    for j in range(i.index(currLoc), (i.index(dest)),-1):
                        self.warehouse.shelvesdictionary[i[j-1]].parentnode = self.warehouse.shelvesdictionary[i[j]].name
                        self.cost = self.cost + 1
                        self.visited.insert(0, self.warehouse.shelvesdictionary[i[j-1]].name)
                    return dest
                else:
                    if self.location != currLoc:
                        self.cost = self.cost + 1
                    for j in range(i.index(currLoc), (i.index(dest))):
                        self.warehouse.shelvesdictionary[i[j+1]].parentnode = self.warehouse.shelvesdictionary[i[j]].name
                        self.cost = self.cost + 1
                        self.visited.insert(0, self.warehouse.shelvesdictionary[i[j+1]].name)
                    return dest
        
                
    def returnToDoor(self, goal):
        reached = True
        node = self.warehouse.shelvesdictionary[goal]
        while reached:
            arr = []
            for i in node.adjacentnodes:
                arr.append(int(i['name']))
            arr.sort()
            node = self.warehouse.shelvesdictionary[str(arr[0])]
            self.cost = self.cost + 1
            self.visited.insert(0, node.name)
            if node.name == '1':
                return False




    
    
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
                self.visited.insert(0,n['loc'])
                self.calculateCost(goal, frontier,n,depthBound)
                return n['loc']
            
            if self.checkPath(str(self.customerOrder.division),n['loc']):
                self.visited.insert(0,n['loc'])
                return self.goToDest(str(self.customerOrder.division), n['loc'])
                
            if n['depth'] < depthBound:
                self.divisions.clearChildNodes(n['loc'])
                self.divisions.generateChildNodes(n['loc'])
                self.divisions.generateParentNodes(n['loc'])
                s = 0
                l = n['depth'] + 1
                for i in self.divisions.divisionsDict[n['loc']].childnodes:
                    frontier.insert(s,{'loc':i.name, 'depth':l})
                    s = s + 1
                    
            self.visited.insert(0,n['loc'])
            self.calculateCost(goal, frontier,n,depthBound)
            
            if len(frontier) == 0:
                frontier.append({'loc':self.location, 'depth':0})
                depthBound = depthBound + 1
                l = 0
    
    #counted forward and backward and combined
    def calculateCost(self,goal,frontier,n,depthBound):
        v = self.visited.pop(0)
        self.visited.insert(0, v)
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
                        self.visited.insert(0, node.parentnode)
                            
        
                #add cost to traverse to other side of the tree
            if len(frontier) > 0 and self.divisions.divisionsDict[node.parentnode].parentnode != '':
                t = node
                while self.divisions.divisionsDict[frontier[0]['loc']].parentnode != t.parentnode and self.divisions.divisionsDict[frontier[0]['loc']].parentnode != t.name :
                    t = self.divisions.divisionsDict[t.parentnode]
                    self.visited.insert(0, t.parentnode)
                    for i in self.divisions.divisionsDict[t.name].adjacentnodes:
                        if i['name'] == t.parentnode:
                            self.cost = self.cost + int(i['cost'])
                
                #add cost to traverse back from right side of tree
            if len(frontier) == 0:
                t = node
                while self.divisions.divisionsDict[t.parentnode].parentnode != '':
                    t = self.divisions.divisionsDict[t.parentnode]
                    self.visited.insert(0, t.parentnode)
                    for i in self.divisions.divisionsDict[t.name].adjacentnodes:
                        if i['name'] == t.parentnode:
                            self.cost = self.cost + int(i['cost'])
                               
            #add cost to traverse back from a node with no children                
            if n['depth'] != depthBound and len(self.divisions.divisionsDict[node.name].childnodes) == 0:
                for i in self.divisions.divisionsDict[node.name].adjacentnodes:
                    if i['name'] == node.parentnode:
                        self.cost = self.cost + int(i['cost'])
                        self.visited.insert(0, node.parentnode)
                            
   
         
    def addToPathMem(self,dest):
        path = []
        node = self.divisions.divisionsDict[dest]
        path.append(node.name)
        while node.parentnode != '':
            node = self.divisions.divisionsDict[node.parentnode]
            path.append(node.name)
        self.pathMem.append(path)
    
    def checkPath(self,dest,currLoc):
        for i in self.pathMem:
            if currLoc in i and dest in i:
                return True
        return False

    def goToDest(self, dest, currLoc):
        for i in self.pathMem:
            if currLoc in i and dest in i:
                if i.index(currLoc) > i.index(dest):
                    if self.location != currLoc:
                        for k in self.divisions.divisionsDict[currLoc].adjacentnodes:
                            if k['name'] == self.divisions.divisionsDict[currLoc].parentnode:
                                self.cost = self.cost + int(k['cost'])
                    for j in range(i.index(currLoc), (i.index(dest)),-1):
                        self.divisions.divisionsDict[i[j-1]].parentnode = self.divisions.divisionsDict[i[j]].name
                        
                        for k in self.divisions.divisionsDict[i[j-1]].adjacentnodes:
                            if k['name'] == self.divisions.divisionsDict[i[j-1]].parentnode:
                                self.cost = self.cost + int(k['cost'])
                                self.visited.insert(0,self.divisions.divisionsDict[i[j-1]].name)
                    return dest
                else:
                    if self.location != currLoc:
                        for k in self.divisions.divisionsDict[currLoc].adjacentnodes:
                            if k['name'] == self.divisions.divisionsDict[currLoc].parentnode:
                                self.cost = self.cost + int(k['cost'])
                    
                    
                    for j in range(i.index(currLoc), (i.index(dest))):
                        
                        self.divisions.divisionsDict[i[j+1]].parentnode = self.divisions.divisionsDict[i[j]].name
                        for k in self.divisions.divisionsDict[i[j+1]].adjacentnodes:
                            if k['name'] == self.divisions.divisionsDict[i[j+1]].parentnode:
                                self.cost = self.cost + int(k['cost'])
                                self.visited.insert(0,self.divisions.divisionsDict[i[j+1]].name)
                    return dest
        
def q5():
    order = customerOrder(rand)
    order.division = '6'
    division = divisions()
    
    af = agentFunction(order, division)
    goal = af.idsDivision()
    print("Division Cost: " + str(af.cost))
    print("Nodes visited: " + str(af.visited))
    
    shelvesOrders = ShelfGenerator(rand)
    shelvesOrders.shelvesOrders.append('33')
    warehouse = Warehouse() 
    
    agent= WarehouseagentFunction(shelvesOrders, warehouse)
    item = agent.idsWarehouse()
    agent.returnToDoor(item)
    print("Warehouse Cost: " + str(agent.cost))
    print("Warehouse Visited: " + str(agent.visited))
    print(str(len(agent.visited)))

def q6():
    
    order = customerOrder(rand)
    division = divisions()
    af = agentFunction(order, division)
    shelvesOrders = ShelfGenerator(rand)
    warehouse = Warehouse() 
    agent= WarehouseagentFunction(shelvesOrders, warehouse)
    visitedDivisionPaths = {}
    totalDivisionCosts = {}
    
    visitedWarehousePaths = {}
    totalWarehouseCosts = {}
    
    for i in range(0,100):
        
        
        
        
        order.generateDivision()
        goal = af.idsDivision()
        af.addToPathMem(goal)
        
        totalDivisionCosts[i] = af.cost
        af.cost = 0
        
        visitedDivisionPaths[i] = af.visited
        af.visited = []
        
        shelvesOrders.generateshelves()
        
        sumvisited = []
        sumcost = 0
        for j in range(0,3): 
            agent.shelfNum = j
            item = agent.idsWarehouse()
            agent.addToWarehousePathMem(item)
            agent.returnToDoor(item)
            sumvisited = sumvisited + agent.visited
            visitedWarehousePaths[str(i) + ':' + str(j)] = agent.visited
            agent.visited = []
            sumcost = sumcost + agent.cost
            totalWarehouseCosts[str(i) + ':' + str(j)] = agent.cost
            agent.cost = 0
        
        visitedWarehousePaths['sum' + str(i)] = sumvisited
        totalWarehouseCosts['sum' + str(i)] = sumcost
     
        
    smallestCostDivision = 0
    smallestCostWarehouseItem = 0 
    smallestCostWarehouse3Item = 0
    
    largestCostDivision = 0
    largestCostWarehouseItem = 0 
    largestCostWarehouse3Item = 0
    
    shortestPathDivision = 0
    shortestPathWarehouseItem = 0
    shortestPathWarehouse3Item = 0
    
    longestPathDivision = 0
    longestPathWarehouseItem = 0
    longestPathWarehouse3Item = 0
    
    averageCostDivision = 0
    averageCostWarehouseItem = 0
    averageCostWarehouse3Item = 0
    
    averagePathDivision = 0
    averagePathWarehouseItem = 0
    averagePathWarehouse3Item = 0
    for i in range(0,100):
        
        
        if (smallestCostDivision == 0):
            smallestCostDivision = totalDivisionCosts[i]
        elif(smallestCostDivision > totalDivisionCosts[i]):
            smallestCostDivision = totalDivisionCosts[i]
        if (largestCostDivision < totalDivisionCosts[i]):
            largestCostDivision = totalDivisionCosts[i]
        averageCostDivision = averageCostDivision + totalDivisionCosts[i]
        
        if (shortestPathDivision == 0):
            shortestPathDivision = len(visitedDivisionPaths[i])
        elif(shortestPathDivision > len(visitedDivisionPaths[i])):
            shortestPathDivision = len(visitedDivisionPaths[i])
        if (longestPathDivision < len(visitedDivisionPaths[i])):
            longestPathDivision = len(visitedDivisionPaths[i])
        averagePathDivision = averagePathDivision + len(visitedDivisionPaths[i])
        
        
        if (smallestCostWarehouse3Item == 0):
            smallestCostWarehouse3Item = totalWarehouseCosts['sum' + str(i)]
        elif(smallestCostWarehouse3Item > totalWarehouseCosts['sum' + str(i)]):
            smallestCostWarehouse3Item = totalWarehouseCosts['sum' + str(i)]
        if (largestCostWarehouse3Item < totalWarehouseCosts['sum' + str(i)]):
            largestCostWarehouse3Item = totalWarehouseCosts['sum' + str(i)]
        averageCostWarehouse3Item = averageCostWarehouse3Item +  totalWarehouseCosts['sum' + str(i)]
            
         
        if (shortestPathWarehouse3Item == 0):
            shortestPathWarehouse3Item = len(visitedWarehousePaths['sum' + str(i)])
        elif(shortestPathWarehouse3Item > len(visitedWarehousePaths['sum' + str(i)])):
            shortestPathWarehouse3Item = len(visitedWarehousePaths['sum' + str(i)])
        if (longestPathWarehouse3Item < len(visitedWarehousePaths['sum' + str(i)])):
            longestPathWarehouse3Item = len(visitedWarehousePaths['sum' + str(i)])
        averagePathWarehouse3Item = averagePathWarehouse3Item + len(visitedWarehousePaths['sum' + str(i)])
            
        
        for j in range(0,3):
            if (smallestCostWarehouseItem == 0):
                smallestCostWarehouseItem = totalWarehouseCosts[str(i) + ':' + str(j)] 
            elif(smallestCostWarehouseItem > totalWarehouseCosts[str(i) + ':' + str(j)] ):
                smallestCostWarehouseItem = totalWarehouseCosts[str(i) + ':' + str(j)] 
            if (largestCostWarehouseItem < totalWarehouseCosts[str(i) + ':' + str(j)] ):
                largestCostWarehouseItem = totalWarehouseCosts[str(i) + ':' + str(j)] 
            averageCostWarehouseItem = averageCostWarehouseItem + totalWarehouseCosts[str(i) + ':' + str(j)]
            
            
            if (shortestPathWarehouseItem  == 0):
                shortestPathWarehouseItem  = len(visitedWarehousePaths[str(i) + ':' + str(j)])
            elif(shortestPathWarehouseItem  > len(visitedWarehousePaths[str(i) + ':' + str(j)])):
                shortestPathWarehouseItem  = len(visitedWarehousePaths[str(i) + ':' + str(j)])
            if (longestPathWarehouseItem < len(visitedWarehousePaths[str(i) + ':' + str(j)])):
                longestPathWarehouseItem = len(visitedWarehousePaths[str(i) + ':' + str(j)])
            averagePathWarehouseItem = averagePathWarehouseItem + len(visitedWarehousePaths[str(i) + ':' + str(j)])
        
    print("Shortest Cost Division: " + str(smallestCostDivision))
    print("Shortest Cost Warehouse Item: " + str(smallestCostWarehouseItem))
    print("Shortest Cost Warehouse 3 Item: " + str(smallestCostWarehouse3Item))
    
    print("Longest Cost Division:" + str(largestCostDivision))
    print("Longest Cost Warehouse Item:" + str(largestCostWarehouseItem))
    print("Longest Cost Warehouse 3 Item:" + str(largestCostWarehouse3Item))
    
    print("Shortest Path Division: " + str(shortestPathDivision))
    print("Shortest Path Warehouse Item: " + str(shortestPathWarehouseItem))
    print("Shortest Path Warehouse 3 Item: " + str(shortestPathWarehouse3Item))
    
    print("Longest Path Division: " + str(longestPathDivision))
    print("Longest Path Warehouse Item: " + str(longestPathWarehouseItem))
    print("Longest Path Warehouse 3 Item: " + str(longestPathWarehouse3Item))
    
    print("Average Cost Division: " + str((averageCostDivision/100)))
    print("Average Cost Warehouse Item: " + str((averageCostWarehouseItem/300)))
    print("Average Cost Warehouse 3 Item: " + str((averageCostWarehouse3Item/100)))
    
    print("Average Path Division: " + str((averagePathDivision/100)))
    print("Average Path Warehouse Item: " + str((averagePathWarehouseItem/300)))
    print("Average Path Warehouse 3 Item: " + str((averagePathWarehouse3Item/100)))
    
        
def main():
   x = input("Enter 5 for Question 5 and Enter 6 for Question 6: ")
   if x == '5':
       q5()
   elif x == '6':
       q6()
   else:
       print("<Input Error>")
   
if __name__ == "__main__":
    main()
    
    