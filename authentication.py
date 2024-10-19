from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from config import Config
from flask_sqlalchemy import SQLAlchemy
import secrets

auth_bp = Blueprint('auth', __name__)

db = SQLAlchemy()

def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]

def validate_csrf_token(token):
    return token == session.get("csrf_token")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        token = request.form.get("csrf_token")
        if not validate_csrf_token(token):
            return "Invalid CSRF token", 403
        
        name = request.form["username"]
        admin = request.form["admin"]
        password = request.form["salasana"]
        hash_value = generate_password_hash(password)

        sql_check = "SELECT 1 FROM accounts WHERE username=:username"
        result = db.session.execute(text(sql_check), {"username": name})
        existing_user = result.fetchone()
        
        if existing_user:
            return "Käyttäjänimi on jo käytössä"
        else:
            sql_insert = "INSERT INTO accounts (username, password, admin) VALUES (:username, :password, :admin)"
            db.session.execute(text(sql_insert), {"username": name, "password": hash_value, "admin": admin})
            db.session.commit()

            flash("Käyttäjä luotu!")
            return redirect(url_for("auth.registration_complete"))

    return render_template("register.html", csrf_token=generate_csrf_token())

@auth_bp.route("/registration_complete")
def registration_complete():
    return render_template("registration_complete.html", csrf_token=generate_csrf_token())

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        token = request.form.get("csrf_token")
        if not validate_csrf_token(token):
            return "Invalid CSRF token", 403

        username = request.form["username"]
        password = request.form["password"]

        sql_accounts_id = text("SELECT accounts.account_id, password FROM accounts WHERE username=:username")
        result = db.session.execute(sql_accounts_id, {"username": username})
        user = result.fetchone()    
        if not user:
            return "Invalid username"
        else:
            hash_value = user.password
            
            if check_password_hash(hash_value, password):
                session['username'] = username
                
                if is_admin():
                    return redirect(url_for("web_dev_page"))
                else:
                    return redirect(url_for("restaurants"))
            else:
                return "Invalid password"
    
    return render_template("login.html", csrf_token=generate_csrf_token())

def is_admin():
    username = session.get('username')
    
    sql_admin = "SELECT admin FROM accounts WHERE username=:username"
    result = db.session.execute(text(sql_admin), {"username": username})
    user_admin = result.fetchone()
    return user_admin is not None and user_admin[0] is True