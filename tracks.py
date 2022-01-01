import json
import utils
import matplotlib.pyplot as plt
import heapq
import math


#path = r"D:\1python\short_tracks.json"

map_size = [300, 300]

def load_tracksfile(path):
    """Return a Tracks object"""
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
    """Return a Tracks object"""
    
    url = 'http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?'\
    'start_point_x='+str(start[0])+'&start_point_y='+str(start[1])+ \
    '&end_point_x='+str(end[0])+'&end_point_y='+str(end[1])+\
    '&min_steps_straight='+str(min_steps_straight)+'&max_steps_straight='+str(max_steps_straight)+\
    '&n_tracks='+str(n_tracks)

    utils.validation_query(start, end, url)

    track_data = utils.request_data(url)
    time = track_data['metadata']['datetime']
    resolution = track_data['metadata']['resolution']
    track = track_data['tracks']

    tracks_object = Tracks(start, end, map_size, time, resolution, track)

    if save == True:
        date_time = time[0:4]+time[5:7]+time[8:13]+time[14:16]+time[17:19]
        file_name = "tracks_"+date_time+'_'+str(n_tracks)+'_'+str(start[0])+'_'+str(start[1])\
        +'_'+str(end[0])+'_'+str(end[1])+'.json'
        with open(file_name,'w') as file_obj:
            json.dump(track_data,file_obj)

    return tracks_object


class SingleTrack:
    """A class to represent a track's information."""
    def __init__(self, start_point, end_point, resolution, chain_code, road_type, terrain, elevation):
        self.start = start_point
        self.end = end_point
        self.cc = chain_code
        self.road = road_type
        self.terrain = terrain
        self.elevation = elevation
        self.distances = []
        self.coordinate_x, self.coordinate_y, self.coordinate = utils.track_coordinates(self.start, self.cc)

        for i in range(len(self.cc)):
            self.distances.append(math.sqrt(((self.elevation[i+1]-self.elevation[i])*0.001)**2 
                                                + resolution**2))

    def __str__(self):
        """Return the print form of object"""
        return "SingleTracks: start at "+str(self.start)+" - "+"{{{}}}".format(str(len(self.cc)))+' steps'

    def __len__(self):
        """Return the number of coordinates in the track, including the start and end points."""
        return len(self.elevation)


    def visualise(self, show = True, filename='my_track.png'):
        """Visualise/save a graph with a distance vs elevation plot."""

        distance = [i for i in range(len(self.elevation))]
       
        plt.subplot(2,2,1)
        plt.xlabel('Distance')
        plt.ylabel('Elevation')
        plt.plot(distance, self.elevation)
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
        """Return a list with coordinates of corners, including the start and end points."""

        corner = []
        corner.append(self.start)
        for i in range(len(self.cc)-1):
            if self.cc[i] != self.cc[i+1]:
                corner.append(self.coordinate[i+1])
        corner.append(self.end)
        return corner

    def distance(self):
        """Return the length (km) for the track"""

        total_distance = 0
        for element in range(len(self.distances)):
            total_distance += self.distances[element]

        return total_distance

    def time(self):
        """Return the time (hours) for the track"""
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
        """Return the emission of CO2 (kg) for the track"""

        co2 = 0
        for i in range(len(self.cc)):
            elevation_change = self.elevation[i+1]-self.elevation[i]
            co2 += utils.co2_emission(self.road[i], self.terrain[i], elevation_change, self.distances[i])
        return co2




class Tracks:
    """A class to represent n tracks' information."""
    def __init__(self, start_poit, end_point, map_size, date_time, resolution, tracks):
        self.start = start_poit
        self.end = end_point
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
        """Return the print form of object"""
        return "Tracks: "+"{{{}}}".format(str(len(self.tracks)))+' from '+str(self.start)+' to '+str(self.end)

    def __len__(self):
        """Return the number of tracks is in the object"""
        return len(self.tracks)

    
    def greenest(self):
        """Return the track of the least CO2 emission"""
        co2 = []
        for i in range(len(self.tracks)):
                                  
            co2.append(self.single_track[i].co2()) 
        
        min_num_index_map_co2 = map(co2.index, heapq.nsmallest(1, co2))
        min_num_index_co2 = list(min_num_index_map_co2)[0]

        return self.single_track[min_num_index_co2]


    def fastest(self):
        """Return the fastest track"""
        time = []
        for i in range(len(self.tracks)):
            time.append(self.single_track[i].time())

        min_num_index_map_time = map(time.index, heapq.nsmallest(1, time))
        min_num_index_time = list(min_num_index_map_time)[0]
        
        return self.single_track[min_num_index_time]


    def shortest(self):
        """Return the shortest track"""
        distance = []
        for i in range(len(self.tracks)):
            distance.append(self.single_track[i].distance())

        min_num_index_map_distance = map(distance.index, heapq.nsmallest(1, distance))
        min_num_index_distance = list(min_num_index_map_distance)[0]

        return self.single_track[min_num_index_distance]


    def get_track(self, x):
        """Return the track x"""
        return self.single_track[x]


    def kmeans(self):

        return



# Check
#local_tracks = load_tracksfile(path)
# tracks = query_tracks(start=(0, 0), end=(15, 15),
# n_tracks=10)

# print(len(tracks))
# print(tracks.greenest())
# print(tracks.fastest())
# print(tracks.shortest())
# print(tracks)
# print(tracks.get_track(5).visualise())
# print(tracks.get_track(5).corners())
# print(tracks.get_track(5).distance())

# print(len(local_tracks))
# print(local_tracks.greenest())
# print(local_tracks.fastest())
# print(local_tracks.shortest())
# print(local_tracks)
# print(local_tracks.get_track(1).visualise())
# print(local_tracks.get_track(1).corners())
# print(local_tracks.get_track(1).distance())