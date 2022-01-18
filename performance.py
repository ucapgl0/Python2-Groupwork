import numpy as np
import matplotlib as plt
from tracks import SingleTrack # TODO this may need to be fixed 

# Run both versions of the clustering scripts 
# For input files with a given number of points ranging from 100 - 10,000
# Plot time against required input with a single plot for both
# Save as performance.png 

N_points = np.logspace(100,10000,5) #Define an array of the number of points 

# Generate the input files with the nmber of points

for N in N_points:      #Loop through all the number of points
    #Generate the input files with a given number of files

        # Generate N-1 random points (x,y) from the sample of points (integers in range 300)  

        chain_code =  zip(np.round(np.random.rand(N-1)*300), np.round(np.random.rand(N-1)*300))

            #TODO check that this works 



    # Run with clustering.py & benchmark 


    # Run with clustering_numpy.py & benchmark 


# Plot both times as a single plot


# Save the plot 