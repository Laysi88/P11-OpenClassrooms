import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        for competition in listOfCompetitions:
            if datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now():
                competition["status"] = "closed"
            else:
                competition["status"] = "open"
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"


def config_app(config):
    app.config.update(config)
    return app


competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    if not any(email["email"] == request.form["email"] for email in clubs):
        flash("this email is not registered")
        return render_template(
            "index.html",
        )
    else:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):

    foundClub = [c for c in clubs if c["name"] == club]
    foundCompetition = [c for c in competitions if c["name"] == competition]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html",
            club=foundClub[0],
            competition=foundCompetition[0],
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=foundClub[0], competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    if placesRequired > int(competition["numberOfPlaces"]):
        flash("Not enough places available")
        return render_template("welcome.html", club=club, competitions=competitions)
    if placesRequired > int(club["points"]):
        flash("Not enough points")
        flash(" You have " + str(club["points"]) + " points")
        return render_template("welcome.html", club=club, competitions=competitions)
    elif placesRequired > 12:
        flash("You can only book a maximum of 12 places")
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
        club["points"] = int(club["points"]) - placesRequired
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/board")
def board():
    list_of_clubs = [club.copy() for club in clubs]
    for club in list_of_clubs:
        club.pop("email", None)
    return render_template("board.html", list_of_clubs=list_of_clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
