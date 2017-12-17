#coding: utf-8 -*-
"""
Created on Mon Oct  9 10:27:13 2017
@author: gy17a3m
"""

#Imported libraries/modules with built in functions.
import matplotlib#2D plotting library
import tkinter#For the creation of the Graphical User Interface.
import random#Allows for random number in a given range.
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot #Used to plot the agents locations in the graph.
import matplotlib.animation
import agentframework#Agent module.
import datetime
import csv#Implements classes to read and write tabular data in CSV format.
import requests#Data url.
import bs4 #Beautiful Soup. Necessary for web scrapping.


num_of_agents = 20 #Controls how many agents there are.
num_of_iterations = 100 #Controls the number of iterartions. 
neighbourhood = 30 #Range for sharing.
agents = [] #List for agents. Empty so that coordinates can be added.
environment=[] #List for environment coordinates. Required for shifting the data into a 2D list. 


def getTimeMS():#Gives the time of how long a section of code takes to run.
     dt = datetime.datetime.now()
     return dt.microsecond + (dt.second * 1000000) + \
     (dt.minute * 1000000 * 60) + (dt.hour * 1000000 * 60 * 60)

#Web scrapping.
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
#Print(td_ys)
#Print(td_xs) 


#Csv reading code which is reading in the in.txt file.
f = open('in.txt', newline='') 
reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
#Each row is an increase in the y-direction and each subsequent value in a row increases the x-direction.
for row in reader:
    rowlist =[]
    for item in row: 
        rowlist.append(float(item)) 
    environment.append(rowlist)              
f.close()

fig = matplotlib.pyplot.figure(figsize = (7, 7))
ax = fig.add_axes([0, 0, 1, 1])#Left, bottom, right, top.

carry_on = True 

for i in range(num_of_agents):#For-loop.
     y = int(td_ys[i].text)#Positions assigned from web scrapping.
     x = int(td_xs[i].text)
     #Assigns cordinates to the list of agents.
     agents.append(agentframework.Agent(environment, agents, neighbourhood, y, x))

carry_on = True   

start = getTimeMS()#Start timer.

def update(frame_number):
    
    fig.clear()#Beginning of animation.
    global carry_on
    
    random.shuffle(agents)

    for i in range (num_of_agents):#For loop.
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)

    total = 0 #Control flow with a set of if-else statements.
    for agent in agents:
        total +=agent.store
    if total >= 10000 :
        carry_on = False
        print ("stopping conditon")  
          
    for i in range (num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y, color = 'white')#Make a scatter plot of x vs y.
        
        matplotlib.pyplot.ylim(0, 299)
        matplotlib.pyplot.xlim(0, 299)
        matplotlib.pyplot.imshow(environment)#Display the environment data.
        
def gen_function(b = [0]):#Stopping condition. For example when a < number of iterations.
    a = 0
    global carry_on
    while (a < num_of_iterations) & (carry_on) :
       yield a			
       a = a + 1 
       

#Function that is connected to the menu of which has an action that when clicked runs the entire event based programming model.
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update,  frames=gen_function, repeat=False)
    canvas.show() 

#GUI which displays the model in a window ("root") with a menu to run the model. 
root = tkinter.Tk() 
root.wm_title("Model")
#Matplotlib canvas embedded within our window and associated with fig, our matplotlib figure)
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1) 
menu_bar= tkinter.Menu(root)#Builds the main window. 
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)
end = getTimeMS()#End timer. Print result.
print("time = " + str(end - start))
tkinter.mainloop()#Sets the GUI waiting for events.
