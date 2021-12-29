import json
import utils
import matplotlib.pyplot as plt
import heapq
import math

path = r"D:\1python\short_tracks.json"

map_size = [300, 300]

def load_tracksfile(path):
    track_data = json.load(open(path))
    start = track_data['metadata']['start']
    end = track_data['metadata']['end']
    time = track_data['metadata']['datetime']
    track = track_data['tracks']

    tracks_object = Tracks(start, end, map_size, time, track)
    return tracks_object



def query_tracks(start=(0, 0), end=(299, 299), min_steps_straight=1, max_steps_straight=6, n_tracks=300, save=True):

    url = 'http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?'\
    'start_point_x='+str(start[0])+'&start_point_y='+str(start[1])+ \
    '&end_point_x='+str(end[0])+'&end_point_y='+str(end[1])+\
    '&min_steps_straight='+str(min_steps_straight)+'&max_steps_straight='+str(max_steps_straight)+\
    '&n_tracks='+str(n_tracks)
    
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

        return "SingleTracks: start at "+str(self.start)+" - "+"{{{}}}".format(str(len(self.cc)))+' steps'

    def __len__(self):

        return len(self.elevation)


    def visualise(self, show = True, filename='my_track.png'):
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
        corner = []
        corner.append(self.start)
        for i in range(len(self.cc)-1):
            if self.cc[i] != self.cc[i+1]:
                corner.append(self.coordinate[i+1])
        corner.append(self.end)
        return corner

    def distance(self):
        total_distance = 0
        for element in range(len(self.distances)):
            total_distance += self.distances[element]

        return total_distance

    def time(self):
        time = 0
        for i in range(len(self.cc)):
            if self.road[i] == 'r':
                time += self.distances[i]/30
            if self.road[i] == 'l':
                time += self.distances[i]/80
            if self.road[i] == 'm':
                time += self.distances[i]/120
        return time

    def co2(self):
        co2 = 0
        for i in range(len(self.cc)):
            elevation_change = self.elevation[i+1]-self.elevation[i]
            co2 += utils.co2_emission(self.road[i], self.terrain[i], elevation_change, self.distances[i])
        return co2


          

    


class Tracks:

    def __init__(self, start_poit, end_point, map_size, date_time, resolution, tracks):
        self.start = start_poit
        self.end = end_point
        self.map_size = map_size
        self.date = date_time
        self.resolution = resolution
        self.tracks = tracks

    def __str__(self):

        return "Tracks: "+"{{{}}}".format(str(len(self.tracks)))+' from '+str(self.start)+' to '+str(self.end)

    def __len__(self):

        return len(self.tracks)

    
    def greenest(self):
        self.single_track = []
        co2 = []
        for i in range(len(self.tracks)):
            self.single_track.append(SingleTrack(self.start, self.end, self.resolution, 
                                    self.tracks[i]['cc'], self.tracks[i]['road'], 
                                    self.tracks[i]['terrain'], self.tracks[i]['elevation']))
                                  
            co2.append(self.single_track[i].co2()) 
        
        min_num_index_map_co2 = map(co2.index, heapq.nsmallest(1, co2))
        min_num_index_co2 = list(min_num_index_map_co2)[0]

        return self.single_track[min_num_index_co2]


    def fastest(self):
        time = []
        for i in range(len(self.tracks)):
            time.append(self.single_track[i].time())

        min_num_index_map_time = map(time.index, heapq.nsmallest(1, time))
        min_num_index_time = list(min_num_index_map_time)[0]
        
        return self.single_track[min_num_index_time]


    def shortest(self):
        distance = []
        for i in range(len(self.tracks)):
            distance.append(self.single_track[i].distance())

        min_num_index_map_distance = map(distance.index, heapq.nsmallest(1, distance))
        min_num_index_distance = list(min_num_index_map_distance)[0]

        return self.single_track[min_num_index_distance]


    def get_track(self, x):
            
        return self.single_track[x]


    def kmeans(self):

        return



# Check
tracks = query_tracks(start=(0, 0), end=(15, 15),
n_tracks=10, save=False)

print(len(tracks))
print(tracks.greenest())
print(tracks.fastest())
print(tracks.shortest())
print(tracks)
print(tracks.get_track(5).visualise())
print(tracks.get_track(5).corners())
