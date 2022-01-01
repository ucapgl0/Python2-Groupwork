import requests

def validation_load(path):
    if path.exist() == False:
        raise ValueError('The path should be vaild')


def validation_query(start, end, url):

    if isinstance(start and end, tuple) == False:
        raise TypeError('The start and end coordinates should be tuple') 
    if isinstance(start[0] and start[1] and end[0] and end[1], (int, float)) == False:
        raise TypeError('The elements of start and end coordinates should be number')
    if start[0] < 0  or start[1] < 0 or end[0] < 0 or end[1] < 0:
        raise ValueError('The coordinates input should be positive')
    if start[0] > 299 or start[1] > 299 or end[0] > 299 or end[1] > 299:
        raise ValueError('The elements of coordinates input should be equal or smaller than 299')
    try:
        requests.get(url, timeout=5)
    except:
        raise ConnectionError('The internet connection is not working')

def request_data(url):

    req = requests.get(url, timeout=30) 

    req_json = req.json()

    return req_json

def track_coordinates(start, cc):
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
