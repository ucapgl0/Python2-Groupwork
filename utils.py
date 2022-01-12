import requests
import mimetypes
import os
import json
import doctest

def validation_load(path):
    """
    Check if the input path is valid and ensure all data needed can be extracted. The path should direct 
    to an existing JSON file, and the content in the file should follow the correct structure. The JSON 
    file contains dictionary structured data with particular keys and values. In addition, attributes of 
    tracks extracted should have correct structure as well. 
    
    Parameters
    ----------
    path: str
        The path for a JSON file.
    """

    # Check the path
    if os.path.isfile(path) == False:
        raise TypeError('The path should be vaild document')
    path_type = mimetypes.guess_type(path)
    if path_type[0] == None:
        raise TypeError('The type of document should be json')
    if path_type[0][-4:] != 'json':
        raise TypeError('The type of document should be json')

    json_data = json.load(open(path))
    if isinstance(json_data, dict) == False:
        raise TypeError('The type of json should be dictionary')
    if 'metadata' not in json_data or 'tracks' not in json_data:
        raise ValueError("The keys of json should include 'metadata' and 'tracks'")
    if isinstance(json_data['metadata'], dict) == False:
        raise TypeError('The type of metadata on json should be dictionary')
    if 'start' not in json_data['metadata'] or 'end' not in json_data['metadata']\
        or 'datetime' not in json_data['metadata'] or 'resolution' not in json_data['metadata']:
        raise ValueError("'start' and 'end' and 'datetime' and 'resolution' should be the keys of json['metadata']")

    # Check the elements of 'metadata'
    start = json_data['metadata']['start']
    end = json_data['metadata']['end']
    resolution = json_data['metadata']['resolution']
    track = json_data['tracks']
    if isinstance(start and end, (tuple, list)) == False:
        raise TypeError('The start and end coordinates in json should be tuple or list') 
    if len(start) != 2 or len(end) != 2:
        raise ValueError('The lenth of coordinate of start and end points in json should be 2')
    if isinstance(start[0] and start[1] and end[0] and end[1], (int, float)) == False:
        raise TypeError('The elements of start and end coordinates in json should be number')
    if start[0] < 0  or start[1] < 0 or end[0] < 0 or end[1] < 0:
        raise ValueError('The coordinates in json should be positive')
    if start[0] > 299 or start[1] > 299 or end[0] > 299 or end[1] > 299:
        raise ValueError('The elements of coordinates in json should be equal or smaller than 299')
    if isinstance(resolution, (int, float)) == False:
        raise TypeError('The distance between two points should be number')
    if resolution <= 0 :
        raise ValueError('The distance between two points should be positive number')

    # Check the track properties
    if isinstance(track, list) == False:
        raise TypeError("The type of value of 'track' should be list")
    for i in range(len(track)):
        if isinstance(track[i], dict) == False:
            raise TypeError("The type of elements of json['tracks'] should be dictionary")
        if 'cc' not in track[i] or 'road' not in track[i] or 'terrain' not in track[i] or 'elevation' not in track[i]:
            raise ValueError("The keys of track should include 'cc' and 'road' and 'terrain' and 'elevation'")
        cc = track[i]['cc']
        road = track[i]['road']
        terrain = track[i]['terrain']
        elevation = track[i]['elevation']
        if isinstance(cc and road and terrain, str) == False:
            raise TypeError('The type of chain code, road and terrain should be string')
        if isinstance(elevation, list) == False:
            raise TypeError('The type of elevation should be list')
        if len(cc) != len(road) or len(cc) != len(terrain):
            raise ValueError('The lenth of chain code, road and terrain should be equal to total steps')
        if len(elevation) != len(cc) + 1:
            raise ValueError('The lenth of elevation should be equal to the number of points which equals to total steps plus 1')

        for j in range(len(cc)):
            if cc[j].isdigit() == False:
                raise TypeError('The chain code should be number')
            if int(cc[j]) < 1 or int(cc[j]) > 4:
                raise ValueError('The range of chain code should be integer 1 to 4')
        for j in range(len(road)):
            if road[j] != 'm' and road[j] != 'l' and road[j] != 'r':
                raise ValueError("The type of road should be 'r', 'l' and 'm' which are residential, local and motorway")
        for j in range(len(terrain)):
            if terrain[j] != 'p' and terrain[j] != 'd' and terrain[j] != 'g':
                raise ValueError("The type of terrain should be 'p', 'g' and 'd' which are paved, gravel or dirt")
        for j in range(len(elevation)):
            if isinstance(elevation[j], (int, float)) == False:
                raise TypeError('The type of elements of elevation should be number')


def validation_query(start, end, min_step, max_step, tracks, url):
    """
    Check if the inputs for the function query_tracks() is valid. The coordinates of starting and 
    end points should be tuples of integers. Those integers should be non-negative and cannot exceed 
    the map size. The user must have internet connection to query from the webapp. 
    
    Parameters
    ----------
    start: tuple of ints
        The starting coordinate of the track
    end: tuple of ints
        The starting coordinate of the track
    url: str
        The address of the road-tracks webapp.
    """

    if isinstance(start and end, (tuple, list)) == False:
        raise TypeError('The start and end coordinates should be tuple or list') 
    if len(start) != 2 or len(end) != 2:
        raise ValueError('The lenth of coordinate of start and end points should be 2')
    if isinstance(start[0] and start[1] and end[0] and end[1], (int, float)) == False:
        raise TypeError('The elements of start and end coordinates should be number')
    if start[0] < 0  or start[1] < 0 or end[0] < 0 or end[1] < 0:
        raise ValueError('The coordinates input should be positive')
    if start[0] > 299 or start[1] > 299 or end[0] > 299 or end[1] > 299:
        raise ValueError('The elements of coordinates input should be equal or smaller than 299')
    if isinstance(min_step and max_step, int) == False:
        raise TypeError('The number of minimum and maximum steps on a particular direction should be integer')
    if isinstance(tracks, int) == False:
        raise TypeError('The number of tracks should be integer')
    try:
        requests.get(url, timeout=30)
    except:
        raise ConnectionError('The internet connection is not working')


def request_data(url):
    """
    Request the resolution, time, and the track from the road-tracks webapp.
    
    Parameters
    ----------
    url: str
        The address of the road-tracks webapp.

    Returns
    -------
    JSON object
        A JSON object obtained from the webapp containing data needed to construct a Track object
    """

    req = requests.get(url, timeout=30) 
    req_json = req.json()
    return req_json

def track_coordinates(start, cc):
    """
    Get the coordinates of points in a track with its chaincode. The chaincode consists of values 
    between 1-4, respectively indicating four directions to move at a certain point.
    
    Parameters
    ----------
    start: tuple of ints
        The starting coordinate of the track
    cc: str
        The chaincode of a track indicating steps in it.

    Returns
    -------
    list of integer
        The list of x_coordinates of all points in the track
    list of integer
        The list of y_coordinates of all points in the track
    list of tuples
        The list of coordinates of all points in the track

    Examples
    --------
    # >>> from tracks import load_tracksfile
    # >>> track = load_tracksfile('./short_tracks.json').single_track[0]
    >>> coordinate_x, coordinate_y, coordinate = track_coordinates((2, 3), '11233344111')
    >>> print(coordinate_x, coordinate_y, coordinate)
    [2, 3, 4, 4, 3, 2, 1, 1, 1, 2, 3, 4] [3, 3, 3, 4, 4, 4, 4, 3, 2, 2, 2, 2] [(2, 3), (3, 3), (4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (1, 3), (1, 2), (2, 2), (3, 2), (4, 2)]
    """
    x = []
    y = []
    coordinates = []
    x.append(start[0])
    y.append(start[1])
    coordinates.append((x[0],y[0]))
    for i in range(len(cc)):
        if cc[i] == '1':
            x.append(x[i]+1)
            y.append(y[i])
        if cc[i] == '2':
            x.append(x[i])
            y.append(y[i]+1)
        if cc[i] == '3':
            x.append(x[i]-1)
            y.append(y[i])
        if cc[i] == '4':
            x.append(x[i])
            y.append(y[i]-1)
        coordinates.append((x[i+1], y[i+1]))

    return x, y, coordinates


def co2_emission(road, terrain, elevation_change, distance):
    """
    Calculate the amount of CO2 emission from one certain point to the next point in a track. The CO2 
    emission between two points depends on the road type, the terrain, and the slope.
    
    Parameters
    ----------
    road: str
        The abbreviation indicating the road type between the two points
    terrain: str
        The abbreviation indicating the terrain between the two points
    elevation_change: int
        The slope between the two points
    distance: float
        The distance between the two points.

    Returns
    -------
    float
        The amount of CO2 emission between the two points

    Examples
    --------
    # >>> from tracks import load_tracksfile
    # >>> track = load_tracksfile('./short_tracks.json').single_track[0]
    >>> co2 = co2_emission('m', 'g', -4, 1.000012499921876)
    >>> print(co2)
    0.10020458065877329
    """
    a_liter_co2 = 2.6391
    if road == 'r':
        factor_road = 1.40
    if road == 'l':
        factor_road = 1
    if road == 'm':
        factor_road = 1.25
    if terrain == 'd':
        factor_terrain = 2.5
    if terrain == 'g':
        factor_terrain = 1.25
    if terrain == 'p':
        factor_terrain = 1
    if elevation_change < -6:
        factor_slope = 0.16
    if elevation_change >= -6 and elevation_change < -2:
        factor_slope = 0.45
    if elevation_change >= -2 and elevation_change <= 2:
        factor_slope = 1
    if elevation_change > 2 and elevation_change <= 6:
        factor_slope = 1.3
    if elevation_change > 6 and elevation_change <= 10:
        factor_slope = 2.35
    if elevation_change > 10:
        factor_slope = 2.90

    co2 = 0.054 * factor_road * factor_terrain * factor_slope * distance * a_liter_co2
    return co2

doctest.testmod()
