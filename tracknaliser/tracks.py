import json
import tracknaliser.utils as utils
import matplotlib.pyplot as plt
import heapq
import math


map_size = [300, 300]


#### LOADING A SET OF RANDOM TRACKS BETWEEN TWO POINTS

def load_tracksfile(path):
    """
    Load tracks from a single JSON file.

    Parameters
    ----------
    path: str
        A path for a JSON file.

    Returns
    -------
    tracks_object: Tracks
        A Tracks object containing data in the file
    """
    utils.validation_load(path)

    track_data = json.load(open(path))
    start = track_data['metadata']['start']
    end = track_data['metadata']['end']
    time = track_data['metadata']['datetime']
    resolution = track_data['metadata']['resolution']
    track = track_data['tracks']

    tracks_object = Tracks(start, end, map_size, time, resolution, track)
    return tracks_object


def query_tracks(start=(0, 0), end=(299, 299), min_steps_straight=1, max_steps_straight=6, n_tracks=300, save=True):
    """
    Find tracks that meet the given requirements from the given start to the given end points.
    
    Parameters
    ----------
    start: tuple of ints, optional
        The starting coordinate of the track
    end: tuple of ints, optional
        The starting coordinate of the track
    min_steps_straight: int, optional
        The number of minimum steps on a particular direction
    max_steps_straight: int, optional
        The number of maximum steps on a particular direction
    n_tracks: int, optional
        The maximum number of tracks to find
    save: bool, optional
        True for saving the obtained data as a JSON file in the current directory, False for not 
        saving a file.

    Returns
    -------
    tracks_object: Tracks
        A Tracks object containing tracks that are found matching the inputs
    """
    
    url = 'http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?'\
    'start_point_x='+str(start[0])+'&start_point_y='+str(start[1])+ \
    '&end_point_x='+str(end[0])+'&end_point_y='+str(end[1])+\
    '&min_steps_straight='+str(min_steps_straight)+'&max_steps_straight='+str(max_steps_straight)+\
    '&n_tracks='+str(n_tracks)

    utils.validation_query(start, end, min_steps_straight, max_steps_straight, 
                                   n_tracks, url)

    # obtain data from the webapp
    track_data = utils.request_data(url)
    time = track_data['metadata']['datetime']
    resolution = track_data['metadata']['resolution']
    track = track_data['tracks']

    tracks_object = Tracks(start, end, map_size, time, resolution, track)

    # save the obtained data to disk with required filename if needed
    if save == True:
        date_time = time[0:4]+time[5:7]+time[8:13]+time[14:16]+time[17:19]
        file_name = "tracks_"+date_time+'_'+str(n_tracks)+'_'+str(start[0])+'_'+str(start[1])\
        +'_'+str(end[0])+'_'+str(end[1])+'.json'
        with open(file_name,'w') as file_obj:
            json.dump(track_data,file_obj)

    return tracks_object

#####

class SingleTrack:
    """
    A class to represent a single track's information.
    
    Parameters
    ----------
    start: tuple of ints
        The (x,y) corrdinates for the starting point of the track
    end: tuple of ints
        The (x,y) corrdinates for the end point of the track
    resolution: int
        The fixed horizontal distance between every two points in the track
    cc: str
        A simplified chain code string (values between 1-4), indicating directions of steps in 
        the track. The length is N-1 for an N-points track
    road: str
        A string with the abbreviated specification of which type of road is used from residential, 
        local and motorway (r, l, m). The length is N-1 for an N-points track
    terrain: str
        A string withthe abbreviiated specifitaion of the state of the road from paved, gravel or 
        dirt (p, g, d). The length is N-1 for an N-points track
    elevation: list of ints
        The elevation of each point in the track, the length is N for an N-points track
    distances: list of floats
        A list of actual travelled distances between every two adjacent points in the track, the 
        length is N-1 for an N-points track
    coordinate_x: list of ints
        A list of x_coordinates of all points in the track, the length is N for an N-points track
    coordinate_y: list of ints
        A list of y_coordinates of all points in the track, the length is N for an N-points track
    coordinate: list of int tuples
        A list of coordinates of all points in the track, including the starting ad end points. 
        The length is N for an N-points track.
    """
    def __init__(self, start_point, end_point, resolution, chain_code, road_type, terrain, elevation):
        """Set up the initial parameters for a single track. """
        self.start = start_point
        self.end = end_point
        self.cc = chain_code
        self.road = road_type
        self.terrain = terrain
        self.elevation = elevation
        self.distances = []
        #Calculate 'real space' coordinates of the track points given track chain code and initial point
        self.coordinate_x, self.coordinate_y, self.coordinate = utils.track_coordinates(self.start, self.cc)

        #Calculate the distances between consecutive points of the track
        for i in range(len(self.cc)):
            self.distances.append(math.sqrt(((self.elevation[i+1]-self.elevation[i])*0.001)**2 
                                                + resolution**2))

    def __str__(self):
        """
        Get the print form of object.
        
        Returns
        -------
        string
            The the print form of a single track

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> track = tracks.single_track[0]
        >>> print(str(track))
        <SingleTracks: start at (2, 3) - {11} steps>
        """
        return "<SingleTracks: start at "+str(self.start)+" - "+"{{{}}}".format(str(len(self.cc)))+' steps>'

    def __len__(self):
        """
        Get the number of coordinates in the track.
        
        Returns
        -------
        int
            The number of coordinates in a single track, including the starting and end points
        
        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> track = tracks.single_track[0]
        >>> print(len(track))
        12
        """
        return len(self.elevation)


    def visualise(self, show = True, filename='my_track.png'):
        """
        Generate two graphs. Visualise/save a graph with a distance vs elevation plot and the 
        coordinates of the path.
        
        Parameters
        ----------
        show: bool, optional
            True for showing the result on the screen, False for saving it on disk as track.png
        filename: str, optional
            The filename using to save the result on disk.
        """
        distance = []
        total_distance = 0
        for i in range(len(self.distances)+1):
            distance.append(total_distance)
            if i < len(self.distances):
                total_distance += self.distances[i]
       
        # the distance vs elevation plot
        plt.subplot(2,2,1)
        plt.xlabel('Distance')
        plt.ylabel('Elevation')
        plt.plot(distance, self.elevation)
        
        # the coordinates of the path
        plt.subplot(2,2,2)
        plt.title('Track')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.plot(self.coordinate_x, self.coordinate_y)
        
        if show == True:
            plt.show()
        else:
            if filename == 'my_track.png':
                plt.savefig('my_track.png')
            else:
                plt.savefig(filename)
        

    def corners(self):
        """
        Find the corners for a track, including the start and end points. The chaincode indicates the 
        step directions. If the direction changes at some point, that point should be a corner.
        
        Returns
        -------
        corner: list of int tuples
            A list with coordinates of corners

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> track = tracks.single_track[0]
        >>> corners = track.corners()
        >>> print(corners)
        [(2, 3), (4, 3), (4, 4), (1, 4), (1, 2), (4, 2)]
        """
        corner = []
        corner.append(self.start)
        for i in range(len(self.cc)-1):
            if self.cc[i] != self.cc[i+1]:
                corner.append(self.coordinate[i+1])
        corner.append(self.end)
        return corner

    def distance(self):
        """
        Calculate the distance for a track.
        
        Returns
        -------
        total_distance: float
            The total lenth (km) for the track

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> track = tracks.single_track[0]
        >>> dis = track.distance()
        >>> print(dis)
        11.000041499764627
        """
        total_distance = 0
        for element in range(len(self.distances)):
            total_distance += self.distances[element]

        return total_distance

    def time(self):
        """
        Calculate the time (hours) for a track. Time depends on the speed, which is influenced the 
        road type.
        
        Returns
        -------
        time: float
            The time (hours) for the track

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> track = tracks.single_track[0]
        >>> time = track.time()
        >>> print(time)
        0.2041674187457495
        """
        time = 0
        speed_residential = 30
        speed_local = 80
        speed_motorway = 120
        for i in range(len(self.cc)):
            if self.road[i] == 'r':
                time += self.distances[i]/speed_residential
            if self.road[i] == 'l':
                time += self.distances[i]/speed_local
            if self.road[i] == 'm':
                time += self.distances[i]/speed_motorway
        return time

    def co2(self):
        """
        Calculate the emission of CO2 (kg) for a track. The CO2 emission between two points depends on 
        the road type, the terrain, and the slope.
        
        Returns
        -------
        co2: float
            The emission of CO2 (kg) for the track

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> track = tracks.single_track[0]
        >>> e_co2 = track.co2()
        >>> print(e_co2)
        2.4449705197624416
        """

        co2 = 0
        for i in range(len(self.cc)):
            elevation_change = self.elevation[i+1]-self.elevation[i]
            co2 += utils.co2_emission(self.road[i], self.terrain[i], elevation_change, self.distances[i])
        return co2




class Tracks:
    """
    A class to represent n tracks' information.
    
    Parameters
    ----------
    start: tuple of ints
        The (x,y) corrdinates for the starting point of the tracks
    end: tuple of ints
        The (x,y) corrdinates for the end point of the tracks
    map_size: tuples of ints
        The map size indicating the maximum values of integers in the coordinates
    date: Datetime
        The date time of the request in ISO8601 format
    resolution: int
        The fixed horizontal distance between every two points in the tracks
    tracks: list of dictionaries
        The list of dictionaries storing the chaincode, elevation, road, and terrain of every 
        single track in the tracks. The length is N for Tracks with N single tracks in it
    single_track: list of SingleTrack object
        The list of every single track in the tracks, the length is N for Tracks with N single 
        tracks in it.
    """
    def __init__(self, start_point, end_point, map_size, date_time, resolution, tracks):
        """Set up the initial parameters for tracks."""
        self.start = (start_point[0], start_point[1])
        self.end = (end_point[0], end_point[1])
        self.map_size = map_size
        self.date = date_time
        self.resolution = resolution
        self.tracks = tracks
        self.single_track = []
        for i in range(len(self.tracks)):
            self.single_track.append(SingleTrack(self.start, self.end, self.resolution, 
                                    self.tracks[i]['cc'], self.tracks[i]['road'], 
                                    self.tracks[i]['terrain'], self.tracks[i]['elevation']))

    def __str__(self):
        """
        Get the print form of object.
        
        Returns
        -------
        string
            The print form of a Tracks object
        
        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> print(str(tracks))
        <Tracks: {5} from (2, 3) to (4, 2)>
        """
        return "<Tracks: "+"{{{}}}".format(str(len(self.tracks)))+' from '+str(self.start)+' to '+str(self.end)+">"

    def __len__(self):
        """
        Get the number of tracks in the object.
        
        Returns
        -------
        int
            The the number of tracks in a Tracks object
        
        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> print(len(tracks))
        5
        """
        return len(self.tracks)

    
    def greenest(self):
        """
        Find the track of the least CO2 emission in a Tracks object.
        
        Returns
        -------
        SingleTrack object
            The track of the least CO2 emission

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> greenest_track = tracks.greenest()
        >>> print(greenest_track)
        <SingleTracks: start at (2, 3) - {5} steps>
        """
        co2 = []
        for i in range(len(self.tracks)):        
            co2.append(self.single_track[i].co2()) 
        
        min_num_index_map_co2 = map(co2.index, heapq.nsmallest(1, co2))
        min_num_index_co2 = list(min_num_index_map_co2)[0]

        return self.single_track[min_num_index_co2]


    def fastest(self):
        """
        Find the fastest track in a Tracks object.
        
        Returns
        -------
        SingleTrack object
            The track of the least time

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> fastest_track = tracks.fastest()
        >>> print(fastest_track)
        <SingleTracks: start at (2, 3) - {5} steps>
        """
        time = []
        for i in range(len(self.tracks)):
            time.append(self.single_track[i].time())

        min_num_index_map_time = map(time.index, heapq.nsmallest(1, time))
        min_num_index_time = list(min_num_index_map_time)[0]
        
        return self.single_track[min_num_index_time]


    def shortest(self):
        """
        Find the shortest track in a Track object.
        
        Returns
        -------
        SingleTrack object
            The track of the shortest distance

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> shortest_track = tracks.shortest()
        >>> print(shortest_track)
        <SingleTracks: start at (2, 3) - {5} steps>
        """
        distance = []
        for i in range(len(self.tracks)):
            distance.append(self.single_track[i].distance())

        min_num_index_map_distance = map(distance.index, heapq.nsmallest(1, distance))
        min_num_index_distance = list(min_num_index_map_distance)[0]

        return self.single_track[min_num_index_distance]


    def get_track(self, x):
        """
        Find a single track in a Tracks object with the index x.
        
        Parameters
        ----------
        x: int
            The index to find a single track in the tracks list.

        Returns
        -------
        SingleTrack object
            The track at index x in the tracks list

        Examples
        --------
        >>> tracks = load_tracksfile('./short_tracks.json')
        >>> target_track = tracks.get_track(3)
        >>> print(target_track)
        <SingleTracks: start at (2, 3) - {5} steps>
        """
        if isinstance(x, int) == False:
            raise TypeError('x should be an integer')
        if x < 0:
            raise ValueError('x should not be negative')
        if x >= len(self.tracks):
            raise ValueError('x should be smaller than the number of tracks')
        return self.single_track[x]


    def kmeans(self,n,cluster_number):
        """
        Call the function to run k-means algorithm.

        Parameters
        ----------
        cluster_number: int
            The parameter indicating the number of cluster centers passed to the algorithm.

        Returns
        -------
        list of tuples
            The results returned by the algorithm
        """
        from clustering import cluster
        kmeans_coordinates=[]
        #create list of coordinates (in tuple form) for kmeans algorithm clustering
        for i in range(len(self.tracks)):
            kmeans_coordinates.append((self.single_track[i].time(),self.single_track[i].distance(),self.single_track[i].co2()))
        #print(len(kmeans_coordinates))
        alloc,m=cluster(kmeans_coordinates,n=10,k=cluster_number)
        # #Visual output
        # from matplotlib import pyplot as plt 
        # fig = plt.figure()
        # ax = fig.add_subplot(projection='3d')
        # for i in range(cluster_number):
        #     alloc_plist = [p for j, p in enumerate(kmeans_coordinates) if alloc[j]==i]
        #     ax.scatter([a[0] for a in alloc_plist],[a[1] for a in alloc_plist],[a[2] for a in alloc_plist])
        # plt.show()
        return alloc,m

# doctest
if __name__=='__main__':
    import doctest
    doctest.testmod()

# # kmeans
# tracks = query_tracks(start=(0, 0), end=(55, 55), n_tracks=100, save=False)
# print(tracks.kmeans(10,3))
