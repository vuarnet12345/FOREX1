#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 10:15:06 2018

@author: amakanwabuikwu
"""

import pandas as pd

import csv

import math

from collections import deque



def filetodictionary():
    calls_df, = pd.read_html("https://finance.yahoo.com/currencies/", header=0, parse_dates=["Symbol"])
    calls_df.to_csv ("data.csv" , index=False)
    
    with open ('data.csv') as csvfile: 
    
        reader =csv.DictReader(csvfile)
        result ={}
        for row in reader:
            pair = row["Symbol"]
            rates = row["Last Price"]
            result[pair]= rates
            
    return result


def makegraph(fdata):
    G = WgtGraph()
    for key in fdata.keys():
        tokens = key.split(':')
        if tokens[0] != tokens[1]:
            G.addEdge(WgtEdge(tokens[0], tokens[1], -math.log(fdata[key])))
            
            return G
        
class WgtEdge(object):
    def __init__(self, v, w, weight):
        self._v = v
        self._w = w
        self._weight = weight

    def fromVertex(self):
        return self._v

    def toVertex(self):
        return self._w

    def weight(self):
        return self._weight

    def __str__(self):
        return "fromVertex: {0}, toVertex: {1}, weight: {2}".format(self._v, self._w, self._weight)
    

class WgtGraph(object):
    def __init__(self):
        self._numEdges = 0
        self._numVertices = 0
        self._adjList = {}
        
    def addEdge(self, graphEdge):
        if not graphEdge.fromVertex() in self._adjList:
            self._adjList[graphEdge.fromVertex()] = []
            self._numVertices += 1
        self._adjList[graphEdge.fromVertex()].append(graphEdge)

        self._numEdges += 1
        
    def neighbors(self, vertex):
        """(str)-> list
        neighbors returns a list of all outgoing edges for the specified vertex
        """
        return self._adjList.get(vertex)

    def vertices(self):
        """()-> list
        vertices returns a list of vertices with outgoing edges
        """ 
        return self._adjList.keys()

    def numVertices(self):
        """()->int"""
        return self._numVertices

    def adjList(self):
        """()->{}"""
        return self._adjList
    
    def __str__(self):
        toString = ""
        for vertex in self.vertices():
            toString += vertex + "\n"
            for edge in self.neighbors(vertex):
                toString += str(edge) + "\n"
        return toString
    
class WgtDirectedCycle(object):
    def __init__(self, G):
        self._explored = set()
        self._edgeTo = {}
        self._onStack = set()
        self._cycle = []
        for vertex in G.vertices():
            if vertex not in self._explored: self.dfs(G, vertex)
    def dfs(self, G, vertex):
        self._onStack.add(vertex)
        self._explored.add(vertex)
        if vertex in G.adjList():
            for edge in G.neighbors(vertex):
                toVertex = edge.toVertex()

                ## short circuit if cycle found
                if self._cycle != []: return 
            
                ## if a new vertex found, recur
                elif toVertex not in self._explored:
                    self._edgeTo[toVertex] = edge
                    self.dfs(G, toVertex)

                elif toVertex in self._onStack:
                    while edge.fromVertex() != toVertex:
                        self._cycle.append(edge)
                        edge = self._edgeTo[edge.fromVertex()]
                    self._cycle.append(edge)

            self._onStack.remove(vertex)

    def hasCycle(self):
        return self._cycle != []

    def cycle(self):
       return self._cycle
    
class BellmanFord(object):
    def __init__(self, G, source):
            self._distTo = dict([(vertex, float('inf')) for vertex in G.vertices()]) 
            self._distTo[source] = 0
            self._edgeTo = {}
            self._onQueue = dict([(vertex, False) for vertex in G.vertices()])
            self._cycle = []
            self._count = 1
            self._q = deque()
            self._q.append(source)
            self._onQueue[source] = True
            while(len(self._q) > 0 and not self.hasNegativeCycle()):
                vertex = self._q.popleft()
                self._onQueue[vertex] = False
                self.relax(G, vertex)
            

    def relax(self, G, vertex):
            epsilon = 0.0001
            for edge in G.neighbors(vertex):
                toVertex = edge.toVertex()  
                if self._distTo[toVertex] > self._distTo[vertex] + edge.weight() + epsilon:
                    self._distTo[toVertex] = self._distTo[vertex] + edge.weight()
                    self._edgeTo[toVertex] = edge
                    if not self._onQueue[toVertex]:
                        self._q.append(toVertex)
                        self._onQueue[toVertex] = True
            self._count += 1
            if self._count % 2*G.numVertices() == 0:
                self.findNegativeCycle()

    def findNegativeCycle(self):
            spt = WgtGraph()
            for edge in self._edgeTo.values():
                spt.addEdge(edge)
                finder = WgtDirectedCycle(spt)
                self._cycle = finder.cycle()

    def hasNegativeCycle(self):
            return self._cycle != []

    def getCycle(self):
            return self._cycle  
    
    
def main():
    fdata = filetodictionary()
    G = makegraph(fdata)
    bf =BellmanFord(G, G.vertices()[0])

    if bf.hasNegativeCycle():
        result = bf.getCycle()
        print ("Start with 100 units {0}".format(result[-1].fromVertex()))
        balance = 100
        while result:
            edge = result.pop()
            key = edge.fromVertex() + "_" + edge.toVertex()
            balance = balance * fdata[key]
            print ("{0} to {1} @ {2} = {3:.2f} {4}".format(edge.fromVertex(), edge.toVertex(), fdata[key], balance, edge.toVertex()))
    else:
        print ("No arbitrage found")
        
    

    
    


        

        

