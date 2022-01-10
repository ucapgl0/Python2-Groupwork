import math
import random

# Checklist of proposed changes:

# 1. import math, random, not as * [x] e0c59b01f9daaa88ce26ebf139c15882ef1c87e5
# 2. Comment explaining what the code does [x]
# 3. Rename some of the variables (e.g. ps) [x] (probably with comments it should be clear enough)
# 4. Use numpy where possible to speedup the code [ ]: 
#     I think that the arrays we deal with here are too small to make numpy performing significantly better... ~Dom

k=3 #The number of clusters of nearby points 

#Reading the file containing points in 3D space
lines = open('samples.csv', 'r').readlines() #read file line by line
ps=[] #point set: list containing each point coordinates (written as a tuple)
for line in lines: #iterate through the line and add each point coordinates
  ps.append(tuple(map(float, line.strip().split(',')))) 

#Pick 3 points at random for the initial cluster centres
m=[ps[random.randrange(len(ps))], ps[random.randrange(len(ps))], ps[random.randrange(len(ps))]]    

alloc=[None]*len(ps)  #list which contains allocates point to one of the three clusters
n=0
while n<10: #iterate the k-means algorithm
  for i in range(len(ps)):  #iterate through the list of all points 
    p=ps[i] #index of the point in the point list
    d=[None] * 3 #list of distances of a point to each of the cluster centres
    d[0]=math.sqrt((p[0]-m[0][0])**2 + (p[1]-m[0][1])**2 + (p[2]-m[0][2])**2) #distance of the point to the 1st cluster
    d[1]=math.sqrt((p[0]-m[1][0])**2 + (p[1]-m[1][1])**2 + (p[2]-m[1][2])**2) #distance of the point to the 2nd cluster
    d[2]=math.sqrt((p[0]-m[2][0])**2 + (p[1]-m[2][1])**2 + (p[2]-m[2][2])**2) #distance of the point to the 3rd cluster
    alloc[i]=d.index(min(d)) #assign the point to the cluster which is the closest to it
  for i in range(3):  #loop through for each of the 3 clusters
    alloc_ps=[p for j, p in enumerate(ps) if alloc[j] == i] #make a list of all points within a given cluster
    #within each cluster find the (virtual) point by averaging over all cluster points
    new_mean=(sum([a[0] for a in alloc_ps]) / len(alloc_ps), sum([a[1] for a in alloc_ps]) / len(alloc_ps), sum([a[2] for a in alloc_ps]) / len(alloc_ps))
    #use such (virtual) point to be a new cluster centre
    m[i]=new_mean
  n=n+1 #repeat the above procedure 10 times


##### OUTPUTING THE ALGORITHM RESULTS 
# Text output
for i in range(3):
  alloc_ps=[p for j, p in enumerate(ps) if alloc[j] == i]
  print("Cluster " + str(i) + " is centred at " + str(m[i]) + " and has " + str(len(alloc_ps)) + " points.")
  print(alloc_ps)

# #Visual output
# from matplotlib import pyplot as plt 
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# for i in range(3):
#   alloc_ps = [p for j, p in enumerate(ps) if alloc[j]==i]
#   ax.scatter([a[0] for a in alloc_ps],[a[1] for a in alloc_ps],[a[2] for a in alloc_ps])
# plt.show()