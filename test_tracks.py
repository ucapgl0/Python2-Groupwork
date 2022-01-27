import pytest
import tracknaliser.tracks as tracks
import tracknaliser.utils as utils



# Tests for converting the chaincode to corner coordinates
@pytest.mark.parametrize('chain_code, start_point, correct_coordinates',[('1232', [2,5], 
[(2,5), (3,5), (3,6), (2,6), (2,7)]), ('14333222', [6,2], 
[(6,2), (7,2), (7,1), (6,1), (5,1), (4,1), (4,2), (4,3), (4,4)]), ('21244111', [3,3], 
[(3,3), (3,4), (4,4), (4,5), (4,4), (4,3), (5,3), (6,3), (7,3)])])

def test_chaincode_conver_to_coordinates(start_point, chain_code, correct_coordinates):
    x, y, coordinate = utils.track_coordinates(start_point, chain_code)
    assert coordinate == correct_coordinates

# Negative test for incorrect path
path_1 = "./samples.csv"
def test_improper_path_input():
    with pytest.raises(TypeError) as exception:
        tracks.load_tracksfile(path_1)

# Negative test for query
def test_improper_type_coordinate_input():
    with pytest.raises(TypeError) as exception:
        tracks.query_tracks(start=('a', 30)) 

def test_negative_coordinate_input():
    with pytest.raises(ValueError) as exception:
        tracks.query_tracks(start=(-1, 20))



# Test the tracks object 
path_2 = "./short_tracks.json"
local_tracks = tracks.load_tracksfile(path_2)

def test_tracks_len():
    assert len(local_tracks) == 5

def test_tracks_print_form():
    assert str(local_tracks) == '<Tracks: {5} from (2, 3) to (4, 2)>'

def test_tracks_greenest():
    assert local_tracks.greenest().co2() == 0.8247902275161714

def test_tracks_fastest():
    assert local_tracks.fastest().time() ==  0.0708340187457662

def test_tracks_shortest():
    assert local_tracks.shortest().distance() ==  5.000038499765378

# Negative test for get_track method
def test_improper_x_for_get_track():
    with pytest.raises(ValueError) as exception:
        local_tracks.get_track(100)

# Test the single_track object
track_1 = local_tracks.get_track(1)

def test_single_track_print_form():
    assert str(track_1) == '<SingleTracks: start at (2, 3) - {9} steps>'

def test_single_track_len():
    assert len(track_1) == 10

def test_single_track_corners():
    assert track_1.corners() == [(2, 3), (2, 1), (1, 1), (1, 0), (4, 0), (4, 2)]

def test_single_track_distance():
    assert track_1.distance() == 9.00006449960888

def test_single_track_time():
    assert track_1.time() == 0.3000021499869626

def test_single_track_co2():
    assert track_1.co2() == 2.1996771881096326

# test mocking services that requires the internet connection
def test_the_internet():
    from unittest import mock
    connection_failed = mock.Mock(return_value=False)
    with pytest.raises(ConnectionError) as e:
        utils.validation_query((0, 0), (299, 299), 1, 6, 300, connection_failed)

pytest.main(["test_tracks.py"])