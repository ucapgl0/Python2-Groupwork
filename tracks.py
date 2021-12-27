import json
import datetime
import requests


def load_tracksfile(path):

    req = requests.get(path, timeout=30) 

    req_jason = req.json()

    return req_jason

file_name = 'afd'
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
    
    track_data = load_tracksfile(url)
    now = datetime.datetime.now()
    single_track = {}
    tracks_object = {}
    N = len(elevation)
    
    for i in range(N):
        single_track[i] = SingleTrack()

    for j in range(n_tracks):
        tracks_object[j] = Tracks(start, end, map_size, now, single_track)

    if save == True:
        date = str(now.strftime("%Y%m%d")+'T'+now.strftime("%H%M%S")+'_')
        file_name = "tracks_"+date+str(n_tracks)+'_'+str(start[0])+'_'+str(start[1])\
        +'_'+str(end[0])+'_'+str(end[1])+'.json'
        with open(file_name) as file_obj:
            json.dump(track_data,file_obj)

    return tracks_object


class SingleTrack:

    def __init__(self, start_point, end_point, chain_code, road_type, terrain, elevation):
        self.start = start_point
        self.end = end_point
        self.cc = chain_code
        self.road = road_type
        self.terrain = terrain
        self.elevation = elevation
    
    def corners(self):
        corners = []
        corners.append(self.start)
        for i in range(len(self.cc)):
            pass
        return

    def visualise(self):
        
        return

    def co2(self):

        return

    def distance(self):

        return

    def time(self):

        return

        
class Tracks:

    def __init__(self, start_poit, end_point, map_size, date, single_track):
        self.start = start_poit
        self.end = end_point
        self.map_size = map_size
        self.date = date
        self.single_track = single_track

    def get_track(self, x):
        
        return

    def greenest(self):

        return

    def fastest(self):

        return

    def shortest(self):

        return
    
    def kmeans(self):

        return