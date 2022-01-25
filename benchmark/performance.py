import numpy as np
import matplotlib as plt
from time import time 
from tracknaliser.clustering import cluster as cluster_list
from tracknaliser.clustering_numpy import cluster as cluster_numpy 

# Run both versions of the clustering scripts 
# For input files with a given number of points ranging from 100 - 10,000
# Plot time against required input with a single plot for both
# Save as performance.png 

num_points = 5

N_points = np.logspace(100,10000,num_points) #Define an array of the number of points 
times = np.zeros((num_points,2)) #array to store the times in 

i = 0 
for N in N_points:      #Loop through all the number of points in the range 
        #Generate the input files with a given number of points

        # Generate N-1 random points (x,y) from the sample of points (integers in range 300)  

        chain_code =  str(zip(np.round(np.random.rand(N-1)*300), np.round(np.random.rand(N-1)*300)))
        elevation = str(np.random.rand(N-1)) #randomly assorted elevations of points in [0,1] range
            #TODO check that this works 
        #Generate the path as a SingleTrack object
        path = SingleTrack((1,1),(299,299),1,chain_code,r,p,elevation)


        # Run with clustering.py & benchmark 

        start_list =time()
        cluster_l = cluster_list(path)
        end_list = time()

        times[i,0] = end_list - start_list #benchmark time
        # Run with clustering_numpy.py & benchmark 
        start_numpy =time()
        cluster_np = cluster_numpy(path)
        end_numpy =time()
        times[i,1] = end_numpy - start_numpy
# Plot both times as a single plot

plt.plot(N_points, times[0], label = "Native python method")
plt.plot(N_points, times[1], label = "Numpy method")
plt.title("Time taken for various input path lengths")
plt.ylabel("Time [s]")
plt.xlabel("N")
plt.legend()
plt.yscale('log')
plt.xscale('log')

# Save the plot 

plt.savefig(r'performamce.png')