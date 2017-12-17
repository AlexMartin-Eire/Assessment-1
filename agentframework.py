# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:17:10 2017

@author: gy17a3m
"""

import random#Allows for random number in a given range.

class Agent():#Agents constructor including environment, agents, neighbourhood and scrapped y, x coordinates from the web.
    def __init__(self, environment, agents, neighbourhood, y, x):#Parameter labels.  
        self.x = 0
        self.y = 0
        if (x == None): #When no coordinate is available a random coordinate is given between 0 and 299. 
            self.x = random.randint(0, 299)
        else:
            self.x = x 
        if (y == None):
            self.y = random.randint(0, 299)
        else:
            self.y = y 
           
        self.agents = agents
        self.environment= environment
        self.store = 0
         
    def move(self):#Move agents one additional step ar else minus one step and never less than 0.5.  
        
        if random.random() < 0.5:
            self.x = (self.x + 1) % 300 #(%)Modulus operator. Prevents agents from falling off the boundary.
        else:
            self.x = (self.x - 1) % 300

        if random.random() < 0.5:
            self.y = (self.y + 1) % 300
        else:
            self.y = (self.y - 1) % 300
            
    def randomize(self):#Random integer.
        self.x = random.randint(0, 299)
        self.y = random.randint(0, 299)
            
    def eat (self):#Agents eat environment and if more than 10 takeaway 10 and store 10.
        
        if self.environment[self.y][self.x]>10:
           self.environment[self.y][self.x]-=10
           self.store+=10
           
    def distance_between(self, agent):# Works out the distance between the two sets of y and x.
     return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5  
 
    #Function to get the agents to search for close neighbours and share resources with them.     
    def share_with_neighbours(self, neighbourhood):
        for agent in self.agents:
            dist = self.distance_between(agent) 
            if dist <= neighbourhood:#If in range of neighbours (<=) share.
                sum = self.store + agent.store
                ave = sum /2 #Add the average sum which is two.
                self.store = ave
                agent.store = ave
                #Print("sharing " + str(dist) + " " + str(ave)) only necessary to check it is working
