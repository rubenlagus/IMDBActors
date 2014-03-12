# -*- coding: utf-8 -*-
'''
Copyright 2014 Ruben Bermudez Lopez

ShortestPath is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

utilidades is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with utilidades.  If not, see <http://www.gnu.org/licenses/>.
'''


class Node():
    ''' Nodes used in Shortestpath algorithm '''
    
    def __init__(self, orig = None, name = None, nodetype = None):
        ''' 
        Constructor
        
        params: 
         * orig: If provide, a copy construction is performed
         * name: Name of the new element to add to current node
         * nodetype: Type of the new element: "f" or "a"
        '''
        if orig is None: # If no copy to make
            self.types = [nodetype] # Add element and type to new node
            self.names = [name]
            self.lastname = name # Set the information of the last element
            self.lasttype = nodetype
            self.length = 0  # Set number of elements in current nodes
        else: # If copy to make
            self.types = list(orig.types) # Make a copy of types list
            self.names = list(orig.names) # Make a copy of names list
            self.length = orig.length+1 # Add one to current length
            self.lastname = name # Update info about last element
            self.lasttype = nodetype
            self.types.append(nodetype) # Append new element and new type
            self.names.append(name)
            
    
    def pushelement(self, element, elementtype):
        ''' 
        Add a new  element
        
        params: 
         * element: New element to add
         * elementtype: Type of element to add: "f" or "a"
        '''
        self.types.append(elementtype)
        self.names.append(element)
        self.lastname = element
        self.lasttype = nodetype
        self.length += 1


class ShortestPath():
    ''' Provide all the functionality needed to make a shortest path search '''
    
    def __init__(self, db, limit = None, ):
        ''' 
        Constructor
        
        params:
         * limit: Limit of the maximum length of path to test (If None, assumed 11)
        '''
        self.listnodes = []
        self.db = db
        if not limit is None:
            self.limit = limit
        else:
            self.limit = 11
    
    def expandNode(self, nodename, nodetype):
        ''' 
        Read all the children of a node
        
        params: 
         * nodename: Element to search children
         * nodetype: Type of current element
         
        note: It use both, the actors DB  and the films DB in other to make it faster
        
        return: If type  is "a" (actor/actress), a list of th films where he/she appears; if "f" (film) a
           list of actors/actresses that appears in it; otherwise, an Exception is raised.
        
        '''
        if nodetype == "a":
            films = self.db.actdb[nodename]
            result = []
            for film in films:
                result.append(film['title'])
            return result
        elif nodetype == "f":
            actors = self.db.filmsdb[nodename]
            return actors
        else:
            raise Exception("Error in the algotithm.")
    
    def findPath(self, origin, destiny):
        ''' 
        Perfoms shortest path search between two actors/actresses
        
        params:
         * origin: Actor/actress at origin 
         * destiny: Actor/actress at end
         
        return: None if any parameter is incorrect, a Node with the path between origin and destiny, or 
           -1 if no path found with length provided
        '''
        if not origin in self.db.actdb['actors']:
            return None
        if not destiny in self.db.actdb['actors']: 
            return None
        
        initnode = Node(name = origin, nodetype = "a")
        self.listnodes = [initnode] # List of nodes to expand
        
        
        while(True):
            currentNode = self.listnodes.pop(0) # Get next node
            if currentNode.length > self.limit: # If length limit, return -1
                return -1
            nextnodes = self.expandNode(currentNode.lastname, currentNode.lasttype) # Expand current node
            for nextnode in nextnodes: # For each element of the expansion
                if currentNode.lasttype == "a": # Set new type
                    nexttype = "f"
                else:
                    nexttype = "a"
                if nexttype == "a" and nextnode == destiny: # If it is a solution, return node
                    return Node(orig=currentNode, name=nextnode, nodetype=nexttype)
                self.listnodes.append(Node(orig=currentNode, name=nextnode, nodetype=nexttype)) # Add new node to list

