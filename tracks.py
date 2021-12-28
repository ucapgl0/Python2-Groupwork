import json
import requests
import utils
import matplotlib.pyplot as plt
import heapq

def request_data(url):

    req = requests.get(url, timeout=30) 

    req_jason = req.json()

    return req_jason


def load_tracksfile(path):
    
    return
# file_name = 'afd'
# a = load_tracksfile('http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?start_point_x=0&start_point_y=0&end_point_x=10&end_point_y=10&min_steps_straight=2&max_steps_straight=10&n_tracks=10')
# print(load_tracksfile('http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?start_point_x=0&start_point_y=0&end_point_x=10&end_point_y=10&min_steps_straight=2&max_steps_straight=10&n_tracks=10'))
# with open(file_name) as file_obj:
#             json.dump(a,file_obj)

map_size = [300, 300]


def query_tracks(start, end, min_steps_straight, max_steps_straight, n_tracks, save):

    url = 'http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?'\
    'start_point_x='+str(start[0])+'&start_point_y='+str(start[1])+ \
    '&end_point_x='+str(end[0])+'&end_point_y='+str(end[1])+\
    '&min_steps_straight='+str(min_steps_straight)+'&max_steps_straight='+str(max_steps_straight)+\
    '&n_tracks='+str(n_tracks)
    
    track_data = request_data(url)
    time = track_data['metadata']['datetime']
    track = track_data['tracks']

    tracks_object = Tracks(start, end, map_size, time, track)

    # if save == True:
    #     date_time = time[0:4]+time[5:7]+time[8:13]+time[14:16]+time[17:19]
    #     file_name = "tracks_"+date_time+'_'+str(n_tracks)+'_'+str(start[0])+'_'+str(start[1])\
    #     +'_'+str(end[0])+'_'+str(end[1])+'.json'
    #     with open(file_name) as file_obj:
    #         json.dump(track_data,file_obj)

    return tracks_object


class SingleTrack:

    def __init__(self, start_point, end_point, chain_code, road_type, terrain, elevation):
        self.start = start_point
        self.end = end_point
        self.cc = chain_code
        self.road = road_type
        self.terrain = terrain
        self.elevation = elevation
    
    def __len__(self):

        return len(self.elevation)


    def visualise(self, show = True, filename='my_track.png'):
        distance = [i for i in range(len(self.elevation))]
        x, y, self.coordinates = utils.track_coordinates(self.start, self.cc)

        plt.subplot(2,2,1)
        plt.xlabel('Distance')
        plt.ylabel('Elevation')
        plt.plot(distance, self.elevation)
        plt.subplot(2,2,2)
        plt.title('Track')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.plot(x,y)

        if show == True:
            plt.show()
        else:
            if filename == 'my_track.png':
                plt.savefig('my_track.png')
            else:
                plt.savefig(filename)
        

    def corners(self):
        corners = []
        corners.append(self.start)
        
        for i in range(1, len(self.cc)):
            if self.cc[i] != self.cc[i-1]:
                corners.append(self.coordinates[i])
        corners.append(self.end)

        return corners

    def distance(self):
        
        len(self.cc)
        return 

    def time(self):
        time = 0
        for i in range(len(self.cc)):
            if self.cc[i] == 'r':
                time += 1/30
            if self.cc[i] == 'l':
                time += 1/80
            if self.cc[i] == 'm':
                time += 1/120
        return time

    def co2(self):
        co2 = 0
        for 
        return

    


class Tracks:

    def __init__(self, start_poit, end_point, map_size, date_time, tracks):
        self.start = start_poit
        self.end = end_point
        self.map_size = map_size
        self.date = date_time
        self.tracks = tracks

    def __len__(self):

        return len(self.tracks)

    
    def greenest(self):
        self.single_track = []
        co2 = []
        for i in range(len(self.tracks)):
            self.single_track.append(SingleTrack(self.start, self.tracks[i]['cc'],
                                    self.tracks[i]['roads'], self.tracks[i]['terrain'],
                                    self.tracks[i]['elevation']))
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


