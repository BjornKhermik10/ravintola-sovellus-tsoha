from flask import Flask
from flask import redirect, render_template, request, session
import os
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = 'tähän secret key'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    opening_hours = db.Column(db.String(255))

@app.route("/restaurants")
def restaurant_list():
    try:
        restaurants = Restaurant.query.all()
        return render_template("restaurants.html", restaurants=restaurants)
    except Exception as e: #jos ei ole esimerkki dataa restaurant tablesissa!
        print(f"Error fetching restaurants: {e}")
        return "An error occurred while fetching restaurants", 500