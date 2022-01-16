import numpy as np 
import random

# Checklist of proposed changes:

# 1. import math, random, not as * [x] e0c59b01f9daaa88ce26ebf139c15882ef1c87e5
# 2. Comment explaining what the code does [x] c2841c373e0e919c6061e2ad943ec498e2c669c6
# 3. Rename some of the variables (e.g. ps) [x] e5d2dbd79b0a5115d95aca0567e4da935a3dd891
# 4. Use numpy where possible to speedup the code [ ]
# 5. Define the cluster function [x]
# 6. Improving readability by explicitly showing dependence on k. [x]

k=3 #The number of clusters of nearby points 

#Reading the file containing points in 3D space
lines = open('samples.csv', 'r').readlines() #read file line by line
parray=np.zeros(len(lines)) # TODo change this to a numpy array point list: list containing each point coordinates (written as a tuple)
for line in lines: #iterate through the line and add each point coordinates
  parray[line] = (tuple(map(float, line.strip().split(',')))) #TODo Change this to an array indexing 

def cluster(parray,n=10):
    #Pick k points at random for the initial cluster centres
    m=[parray[random.randrange(len(parray))] for it in range(0,k)] #TODO change this from list comprehension to array indexing 
    #m=[parray[random.randrange(len(parray))], parray[random.randrange(len(parray))], parray[random.randrange(len(parray))]]    

    alloc=[None]*parray.shape[0]  # TODo change this to parray.shape[0] list which contains allocates point to one of the three clusters
    n=0
    while n<10: #iterate the k-means algorithm
        for i in range(len(parray)):  #iterate through the list of all points 
            p=parray[i] #index of the point in the point list
            d=[None] * k #list of distances of a point to each of the cluster centres
            for q in range(0,k):
                d[q]=np.sqrt((p[0]-m[q][0])**2 + (p[1]-m[q][1])**2 + (p[2]-m[q][2])**2) #distance of the point to the q-th cluster
            alloc[i]=d.index(min(d)) #assign the point to the cluster which is the closest to it

        for i in range(k):  #loop through for each of the k clusters
            alloc_parray=[p for j, p in np.ndenumerate(parray) if alloc[j] == i] # TODo change this from enumerate make a list of all points within a given cluster
            #within each cluster find the (virtual) point by averaging over all cluster points
            new_mean=(sum([a[0] for a in alloc_parray]) / len(alloc_parray), sum([a[1] for a in alloc_parray]) / len(alloc_parray), sum([a[2] for a in alloc_parray]) / len(alloc_parray))
            #use such (virtual) point to be a new cluster centre
            m[i]=new_mean
        n=n+1 #repeat the above procedure 10 times
    return alloc,m

alloc,m=cluster(parray) #TODO change these indexes
# print(alloc)

##### OUTPUTING THE ALGORITHM RESULTS 
# # Text output
# for i in range(k):
#   alloc_parray=[p for j, p in enumerate(parray) if alloc[j] == i]
#   print("Cluster " + str(i) + " is centred at " + str(m[i]) + " and has " + str(len(alloc_parray)) + " points.")
#   print(alloc_parray)

# #Visual output
# from matplotlib import pyplot as plt 
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# for i in range(k):
#   alloc_parray = [p for j, p in enumerate(parray) if alloc[j]==i]
#   ax.scatter([a[0] for a in alloc_parray],[a[1] for a in alloc_parray],[a[2] for a in alloc_parray])
# plt.show()