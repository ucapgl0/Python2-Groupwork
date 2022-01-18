import argparse
import datetime
from tracknaliser.tracks import query_tracks

def process():
    """Set the command line arguments."""
    parser = argparse.ArgumentParser(prog='greentrack', description='Find the greenest path.')

    parser.add_argument('--start', nargs=2, type=int, default=[0,0], help='coordinate of the starting point, default (0, 0)')
    parser.add_argument('--end', nargs=2, type=int, default=[299,299], help='coordinate of the end point, default (299, 299)')
    parser.add_argument('--verbose', action='store_true', help='increase output verbosity')

    args = parser.parse_args()
    try:
        tracks = query_tracks(start=(args.start[0],args.start[1]), end=(args.end[0],args.end[1]), n_tracks=50, save=False)
    except Exception as e:
        parser.error(e)     # print out the error messages
    greenest_track = tracks.greenest()

    # values needed for calculations
    corners = greenest_track.corners()
    co2 = round(greenest_track.co2(),2)
    time = datetime.timedelta(seconds=round(greenest_track.time()*3600))      # to be improve...
    directions = []     # do not have a direction at the end point, so the number of elements is 1 less than the number of corners
    distances = []     # do not have a distance at the end point, so the number of elements is 1 less than the number of corners
    towards = []     # do not need to turn at the starting and end points, so the number of elements is 2 less than the number of corners

    # calculate the directions and distances at corners
    index_pr = 0     # the previous corner's index in the track
    for i in range(1,len(corners)):
        dis = 0     # the distance from one corner to the next corner
        index_diff = abs(corners[i][0]-corners[i-1][0])+abs(corners[i][1]-corners[i-1][1])     # the difference between the two index
        for k in range(index_pr, index_pr+index_diff):
            dis += greenest_track.distances[k]
        distances.append(round(dis))
        index_pr += index_diff     # in the next calculation, the later corner becomes the previous one

        # Find the directions by coordinates of corners
        if corners[i-1][0] == corners[i][0] and corners[i-1][1] < corners[i][1]:
            directions.append('north')
            if i != len(corners)-1 and corners[i][0] < corners[i+1][0]:
                towards.append('right')
            elif i != len(corners)-1 and corners[i][0] > corners[i+1][0]:
                towards.append('left')
        elif corners[i-1][0] == corners[i][0] and corners[i-1][1] > corners[i][1]:
            directions.append('south')
            if i != len(corners)-1 and corners[i][0] < corners[i+1][0]:
                towards.append('left')
            elif i != len(corners)-1 and corners[i][0] > corners[i+1][0]:
                towards.append('right')
        elif corners[i-1][1] == corners[i][1] and corners[i-1][0] < corners[i][0]:
            directions.append('east')
            if i != len(corners)-1 and corners[i][1] < corners[i+1][1]:
                towards.append('left')
            elif i != len(corners)-1 and corners[i][1] > corners[i+1][1]:
                towards.append('right')
        elif corners[i-1][1] == corners[i][1] and corners[i-1][0] > corners[i][0]:
            directions.append('west')
            if i != len(corners)-1 and corners[i][1] < corners[i+1][1]:
                towards.append('right')
            elif i != len(corners)-1 and corners[i][1] > corners[i+1][1]:
                towards.append('left')

    # print out the message
    if args.verbose:
        print('Path:\n- Start from '+str(corners[0]))
        for i in range(len(corners)-2):
            print('- Go '+directions[i]+' for '+str(distances[i])+' km, turn '+towards[i]+' at '+str(corners[i+1]))
        print('- Go '+directions[-1]+' for '+str(distances[-1])+' km,\n- reach your destination at '+\
            str(corners[-1])+'\nCO2: '+str(co2)+' kg\nTime: '+str(time))
    else:
        print('Path: '+str(corners)[1:-1]+'\nCO2: '+str(co2)+' kg\nTime: '+str(time))

if __name__ == "__main__":
    process()