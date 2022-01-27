import math
import random
import argparse

# Checklist of proposed changes:

# 1. import math, random, not as * [x] e0c59b01f9daaa88ce26ebf139c15882ef1c87e5
# 2. Comment explaining what the code does [x] c2841c373e0e919c6061e2ad943ec498e2c669c6
# 3. Rename some of the variables (e.g. ps) [x] e5d2dbd79b0a5115d95aca0567e4da935a3dd891
# 4. Use numpy where possible to speedup the code [ ]
# 5. Define the cluster function [x] 94b51d498c123896b9e6dce3f68c49b9148d7cc0
# 6. Improving readability by explicitly showing dependence on k. [x] 94b51d498c123896b9e6dce3f68c49b9148d7cc0


def cluster(plist,n=10,k=3):
    """
    Group the data points into k clusters.

    Parameters
    ----------
    plist: list of int tuples
        The coordinates of the data points
    n: int
        The number of iterations
    k: int
        The number of cluster centers.

    Returns
    -------
    list of int lists
        The lists with the points indices that belong to each group
    list of ints
        The indices of clusters in which each data point is grouped
    list of float tuples
        The coordinates of clusters centers
    """
    #Pick k points at random for the initial cluster centres
    m=[plist[random.randrange(len(plist))] for it in range(0,k)]

    alloc=[None]*len(plist)  #list which contains allocates point to one of the three clusters
    index = []  # list storing each point's index
    N=0
    while N<n: #iterate the k-means algorithm
        for i in range(len(plist)):  #iterate through the list of all points 
            p=plist[i] #index of the point in the point list
            index.append(i)
            d=[None] * k #list of distances of a point to each of the cluster centres
            for q in range(0,k):
                d[q]=math.sqrt((p[0]-m[q][0])**2 + (p[1]-m[q][1])**2 + (p[2]-m[q][2])**2) #distance of the point to the q-th cluster
            alloc[i]=d.index(min(d)) #assign the point to the cluster which is the closest to it
        for i in range(k):  #loop through for each of the k clusters
            alloc_plist=[p for j, p in enumerate(plist) if alloc[j] == i] #make a list of all points within a given cluster
            #within each cluster find the (virtual) point by averaging over all cluster points
            if len(alloc_plist)!=0:
                new_mean=(sum([a[0] for a in alloc_plist]) / len(alloc_plist), sum([a[1] for a in alloc_plist]) / len(alloc_plist), sum([a[2] for a in alloc_plist]) / len(alloc_plist))
            else: #if no point was assigned to a cluster, set cluster centre position to [0,0,0]
                new_mean=[0,0,0]
            #use such (virtual) point to be a new cluster centre
            m[i]=new_mean
        N=N+1 #repeat the above procedure 10 times

    alloc_i= []   # a list with the points indices that belong to each group
    for i in range(k):
        alloc_p=[p for j, p in enumerate(list(set(index))) if alloc[j] == i]
        alloc_i.append(alloc_p)

    return alloc_i,alloc,m


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("file", type=str, help='Specify the input file')
    parser.add_argument('--iters', nargs=1, type=int, default=[10], help='Specify the number of iterations')
    args = parser.parse_args()

    #Reading the file containing points in 3D space
    try:
        lines = open(args.file, 'r').readlines() #read file line by line
    except Exception as ee:
        parser.error(ee)
    plist=[] #point list: list containing each point coordinates (written as a tuple)
    for line in lines: #iterate through the line and add each point coordinates
        plist.append(tuple(map(float, line.strip().split(','))))
    
    k=3 #The number of clusters of nearby points 
    alloc_i,alloc,m=cluster(plist,n=args.iters[0],k=k)

    #### OUTPUTING THE ALGORITHM RESULTS 
    # Text output
    for i in range(k):
        alloc_plist=[p for j, p in enumerate(plist) if alloc[j] == i]
        print("Cluster " + str(i) + " is centred at " + str(m[i]) + " and has " + str(len(alloc_plist)) + " points.")

    # #Visual output
    # from matplotlib import pyplot as plt 
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # for i in range(k):
    #   alloc_plist = [p for j, p in enumerate(plist) if alloc[j]==i]
    #   ax.scatter([a[0] for a in alloc_plist],[a[1] for a in alloc_plist],[a[2] for a in alloc_plist])
    # plt.show()