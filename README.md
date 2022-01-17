# Introduction

This is the tracknaliser package by working group 20 as the second assignment of 2021-22
[Research Software Engineering with Python](development.rc.ucl.ac.uk/training/engineering) course.

## Installation

```bash
cd tracknaliser-Working-Group-20
pip install .
```

<!-- ## Usage
    
Invoke the tool with `greet <FirstName> <Secondname>` or use it on your own library:

```python
from greeting import greeter

greeter.greet(user.name, user.lastname)
``` -->

# Brief Description

Several people in your lab are involved in a project to study a number of locations on a map. However, the topography changes every day, and each of you have to visit different locations to take some ectoplasm samples.

[webapp]: https://ucl-rse-with-python.herokuapp.com/road-tracks/

Working with a webapp ([https://ucl-rse-with-python.herokuapp.com/road-tracks/][webapp]) which provides multiple different tracks that go from one point to another on these quickly changing lands, this tool does some analysis on the tracks and aims to provide some kind of recommendation to our colleagues. 

## Library-style Interface

We offer a python library to analyse the output JSON file from the webapp, and add functions to give the suggestion based on the most environmentally-friendly of them all, or the fastest, or the shortest, or if you want to explore similar paths. 

For more details, please refer to the documentation page.

## Command Line Interface

In addition, we create a command line tool that gives the coordinates, the travel time and the CO$_{2}$ emissions for the greenest trip.

<!-- ## Usage -->
    
Invoke the tool with `greentrack --start <x coord> <y coord> --end <x coord> <y coord> [--verbose]`

## K-means Algorithm

There is a [k-means algorithm](https://en.wikipedia.org/wiki/K-means_clustering) given by our post-doc works which groups the data points into clusters. 

With a group of points (each point is represented as a tuple of its coordinates), the algorithm proceeds to form three clusters of
nearby points. In the end, each cluster will (ideally) contain points that are close to each other, and far from the other clusters. The code (`clustering.py`) then prints some basic statistics about the resulting clusters.

This algorithm is included in the library, and we do refactoring to make te code more efficient.