from  random import *
import numpy as np
import argparse

# Checklist of proposed changes:

# 1. import math, random, not as * [x] e0c59b01f9daaa88ce26ebf139c15882ef1c87e5
# 2. Comment explaining what the code does [x] c2841c373e0e919c6061e2ad943ec498e2c669c6
# 3. Rename some of the variables (e.g. ps) [x] e5d2dbd79b0a5115d95aca0567e4da935a3dd891
# 4. Use numpy where possible to speedup the code [x]
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
    list of float tuples
        The coordinates of clusters centers
    """
    parray=np.array(plist) #create a numpy array from the data
    centers = []
    for i in range(k):
        centers.append(parray[randrange(len(parray))])
    centers = np.array(centers)
    alloc = np.array([None] * len(parray))
    alloc_l = []
    for i in range(n):
        alloc=np.argmin(np.linalg.norm(parray-centers[:,None],axis=2),axis=0)
        for ii in range(k):
            alloc_p = parray[np.argwhere(alloc == ii)]
            centers[ii] = np.mean(alloc_p,axis=0)
            if i == n-1:
                alloc_i = []
                for j in range(len(alloc)):
                    if alloc[j] == ii:
                        alloc_i.append(j)
                alloc_l.append(alloc_i)
        
    return alloc_l, centers

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
    alloc_i, center = cluster(plist,n=args.iters[0],k=k)

    #### OUTPUTING THE ALGORITHM RESULTS 
    # Text output
    for i in range(k):
      print("Cluster " + str(i) + " is centred at " + str(center[i]) +
       " and contains points" + str(alloc_i[i]))

      # #Visual output
      # from matplotlib import pyplot as plt 
      # fig = plt.figure()
      # ax = fig.add_subplot(projection='3d')
      # for i in range(k):
      #   alloc_plist = [p for j, p in enumerate(plist) if alloc[j]==i]
      #   ax.scatter([a[0] for a in alloc_plist],[a[1] for a in alloc_plist],[a[2] for a in alloc_plist])
      # plt.show()