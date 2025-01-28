from .conftest import client
import json
import pytest


# test route / with status code 200
def test_index_status_code_200(client):
    response = client.get("/")
    assert response.status_code == 200


# test route /showSummary with status code 200
def test_connexion_status_code_200(client):
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200


# test route /showSummary with wrong email
def test_connexion_redirect_with_wrong_email(client):
    response = client.post("/showSummary", data={"email": "admin@irontemple.fr"})
    assert "this email is not registered" in response.data.decode("utf-8")
    assert response.status_code == 200


# test can't book in passed competition
def test_cant_book_in_passed_competition(client):
    data = {"competition": "Spring Festival", "club": "Simply Lift", "places": 5}
    response = client.get("book/Spring%20Festival/Simply%20Lift")
    assert "Compétition déjà passée" in response.data.decode()
    assert response.status_code == 200


# test route /logout with status code 302 and redirection to /index
def test_logout_status_code_302(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


# test route /board with status code 200
def test_board_status_code_200(client):
    response = client.get("/board")
    assert response.status_code == 200


# test /book with status code 200
def test_book_status_code_200(client):
    response = client.get("/book/Fall Classic/Iron Temple")
    assert response.status_code == 200


# test /book with competition or club not found
def test_fail_message_if_club_or_comp_not_found(client):
    response = client.get("/book/Fall Clasc/Iron Temple")
    assert "Something went wrong-please try again" in response.data.decode()
    assert response.status_code == 200


# test status code 200 for purchase place
def test_purchase_status_code_200(client):
    data = {"competition": "Fall Classic", "club": "Iron Temple", "places": 2}
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 200
    assert "Great-booking complete!"


# test no more 12 places can be booked
def test_purchase_more_than_12_places(client):
    data = {"competition": "Summer Classic", "club": "Simply Lift", "places": 13}
    response = client.post("/purchasePlaces", data=data)
    assert "You can only book a maximum of 12 places" in response.data.decode()
    assert response.status_code == 200


# test not enough points
def test_purchase_not_enough_points(client):
    data = {"competition": "Fall Classic", "club": "Iron Temple", "places": 8}
    response = client.post("/purchasePlaces", data=data)
    assert "Not enough points" in response.data.decode()
    assert " You have " in response.data.decode()
    assert response.status_code == 200


# test logout
def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
