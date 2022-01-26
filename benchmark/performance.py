import numpy as np
from matplotlib import pyplot as plt
from time import time
# #import functions from tracknaliser
import sys
sys.path.append('.')
from tracknaliser.clustering import cluster as cluster_list
from tracknaliser.clustering_numpy import cluster as cluster_numpy
# Run both versions of the clustering scripts
# Plot time against required input with a single plot for both
# Save as performance.png
N_points = np.arange(100, 10001, 100)
np.random.seed(0)
test_point = np.random.random_sample((10000,3)) #Define an array of the number of points 
times = np.zeros((2,len(N_points)), dtype=float) #array to store the times in 

for i in range(len(N_points)):
        # Run with clustering.py & benchmark 
        start_list =time()
        cluster_l = cluster_list(test_point[0:100*(i+1)])
        end_list = time()
        times[0][i] = end_list - start_list

        # Run with clustering_numpy.py & benchmark 
        start_numpy =time()
        cluster_np = cluster_numpy(test_point[0:100*(i+1)])
        end_numpy =time()
        times[1][i] = end_numpy - start_numpy

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
plt.savefig('benchmark/performamce.png')
plt.show()