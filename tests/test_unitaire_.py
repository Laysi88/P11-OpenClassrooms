from .conftest import client
import json
import pytest
from server import loadClubs, loadCompetitions


# test load clubs
def test_load_clubs(client):
    club = loadClubs()
    assert club[1] == {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}


# test load competitions
def test_load_competitions(client):
    competition = loadCompetitions()
    assert competition[1] == {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13",
        "status": "closed",
    }
