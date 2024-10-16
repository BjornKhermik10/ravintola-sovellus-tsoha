from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import render_template, request, redirect, url_for, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.config['DEBUG'] = True

COLOR_MAP = {
    1: "#FA6F6F",  # Red
    2: "#5CAEFA",  # Blue
    3: "#006D05",  # Green
    4: "#CA66F8",  # Purple
    5: "#808080",  # Grey
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
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
            return redirect(url_for("registration_complete"))

    return render_template("register.html")

@app.route("/registration_complete")
def registration_complete():
    return render_template("registration_complete.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql_accounts_id = text("SELECT accounts.account_id, password FROM accounts WHERE username=:username")
        result = db.session.execute(sql_accounts_id, {"username":username})
        user = result.fetchone()    
        if not user:
            "Invalid username"
        else:
            hash_value = user.password
            
            if check_password_hash(hash_value, password):
                session['username'] = username
                
                if is_admin():
                    return redirect(url_for("web_dev_page"))
                else:
                    return redirect(url_for("restaurants"))
            else:
                "Invalid password"
            
    
    return render_template("login.html")

def is_admin():
    username = session.get('username')
    
    sql_admin = "SELECT admin FROM accounts WHERE username=:username"
    result = db.session.execute(text(sql_admin), {"username": username})
    user_admin = result.fetchone()
    return user_admin is not None and user_admin[0] is True

@app.route("/restaurants", methods=["GET"])
def restaurants():
    search_sql_query = request.args.get("search", "")
    sql_query = """
        SELECT r.restaurant_id, r.name, r.description, r.opening_hours, 
               COALESCE(AVG(rv.rating), 0) AS average_rating,
               g.group_name, g.color_id
        FROM restaurants r
        LEFT JOIN review rv ON r.restaurant_id = rv.restaurant_id
        LEFT JOIN group_restaurants gr ON r.restaurant_id = gr.restaurant_id
        LEFT JOIN groups g ON gr.group_id = g.group_id
        WHERE r.name ILIKE :search_sql_query
        GROUP BY r.restaurant_id, g.group_name, g.color_id
        ORDER BY average_rating DESC
    """

    result = db.session.execute(text(sql_query), {"search_sql_query": f"%{search_sql_query}%"})
    restaurants = result.fetchall()

    #testing please work - tämä on groups badgejen toimivuutta varten
    restaurant_list = []
    current_restaurant = None
    for row in restaurants:
        if current_restaurant is None or current_restaurant['restaurant_id'] != row.restaurant_id:
            if current_restaurant:
                restaurant_list.append(current_restaurant)
            current_restaurant = {
                'restaurant_id': row.restaurant_id,
                'name': row.name,
                'description': row.description,
                'opening_hours': row.opening_hours,
                'average_rating': row.average_rating,
                'groups': []
            }
        if row.group_name:
            current_restaurant['groups'].append({
                'group_name': row.group_name,
                'color_id': row.color_id
            })
    
    if current_restaurant:
        restaurant_list.append(current_restaurant)

    return render_template("restaurants.html", restaurants=restaurant_list, COLOR_MAP=COLOR_MAP)

@app.route("/web_dev_page", methods=["GET"])
def web_dev_page():
    if is_admin():
        search_sql_query = request.args.get("search", "")
        sql_query = """
            SELECT r.restaurant_id, r.name, r.description, r.opening_hours, 
                COALESCE(AVG(rv.rating), 0) AS average_rating,
                g.group_name, g.color_id
            FROM restaurants r
            LEFT JOIN review rv ON r.restaurant_id = rv.restaurant_id
            LEFT JOIN group_restaurants gr ON r.restaurant_id = gr.restaurant_id
            LEFT JOIN groups g ON gr.group_id = g.group_id
            WHERE r.name ILIKE :search_sql_query
            GROUP BY r.restaurant_id, g.group_name, g.color_id
            ORDER BY average_rating DESC
        """

        result = db.session.execute(text(sql_query), {"search_sql_query": f"%{search_sql_query}%"})
        restaurants = result.fetchall()

        restaurant_list = []
        current_restaurant = None
        for row in restaurants:
            if current_restaurant is None or current_restaurant['restaurant_id'] != row.restaurant_id:
                if current_restaurant:
                    restaurant_list.append(current_restaurant)
                current_restaurant = {
                    'restaurant_id': row.restaurant_id,
                    'name': row.name,
                    'description': row.description,
                    'opening_hours': row.opening_hours,
                    'average_rating': row.average_rating,
                    'groups': []
                }
            if row.group_name:
                current_restaurant['groups'].append({
                    'group_name': row.group_name,
                    'color_id': row.color_id
                })
        
        if current_restaurant:
            restaurant_list.append(current_restaurant)

        return render_template("web_dev_page.html", restaurants=restaurant_list, COLOR_MAP=COLOR_MAP)
    else:
        return "Ei tänne päin!" 

@app.route("/edit_groups", methods=["GET"])
def edit_groups():
    sql_query = """SELECT g.group_id, g.group_name, g.color_id, r.restaurant_id, r.name
        FROM groups g
        LEFT JOIN group_restaurants gr ON g.group_id = gr.group_id
        LEFT JOIN restaurants r ON gr.restaurant_id = r.restaurant_id
        ORDER BY g.group_id"""
    result = db.session.execute(text(sql_query))
    groups = result.fetchall()

    group_data = {}
    for row in groups:
        group_id = row.group_id
        if group_id not in group_data:
            group_data[group_id] = {
                "group_id": group_id,
                "group_name": row.group_name,
                "color_id": row.color_id,
                "restaurants": []
            }
        if row.restaurant_id:
            group_data[group_id]["restaurants"].append({
                "restaurant_id": row.restaurant_id,
                "name": row.name
            })

    return render_template("edit_groups.html", group_data=group_data, COLOR_MAP=COLOR_MAP)

@app.route("/create_group", methods=["GET", "POST"])
def create_group():
    if request.method == "POST":
        group_name = request.form["group_name"]
        color_id = request.form["color_id"]
        selected_restaurants = request.form.getlist("restaurants")

        if len(group_name) > 20:
            flash("Group name must be under 20 characters.")
            return redirect(url_for("create_group"))

        sql_insert_group = "INSERT INTO groups (group_name, color_id) VALUES (:group_name, :color_id) RETURNING group_id"
        result = db.session.execute(text(sql_insert_group), {"group_name": group_name, "color_id": color_id})
        group_id = result.fetchone()[0]
        
        for restaurant_id in selected_restaurants:
            db.session.execute(text("INSERT INTO group_restaurants (group_id, restaurant_id) VALUES (:group_id, :restaurant_id)"),
                               {"group_id": group_id, "restaurant_id": restaurant_id})
        
        db.session.commit()
        flash("Group created successfully!")
        return redirect(url_for("edit_groups"))

    colors = COLOR_MAP.items()
    sql_query = "SELECT restaurant_id, name FROM restaurants"
    result = db.session.execute(text(sql_query))
    restaurants = result.fetchall()

    return render_template("create_group.html", colors=colors, restaurants=restaurants)

@app.route("/add_restaurants_to_group", methods=["GET", "POST"])
def add_restaurants_to_group():
    if request.method == "POST":
        group_id = request.form["group_id"]
        selected_restaurants = request.form.getlist("restaurants")

        for restaurant_id in selected_restaurants:
            existing_entry = db.session.execute(
                text("SELECT COUNT(*) FROM group_restaurants WHERE group_id = :group_id AND restaurant_id = :restaurant_id"),
                {"group_id": group_id, "restaurant_id": restaurant_id}
            ).scalar()

            if existing_entry == 0:
                db.session.execute(
                    text("INSERT INTO group_restaurants (group_id, restaurant_id) VALUES (:group_id, :restaurant_id)"),
                    {"group_id": group_id, "restaurant_id": restaurant_id}
                )

        db.session.commit()
        flash("Ravintolat lisätty ryhmään!")
        return redirect(url_for("edit_groups"))

    sql_query_groups = "SELECT group_id, group_name FROM groups"
    result_groups = db.session.execute(text(sql_query_groups))
    groups = result_groups.fetchall()

    sql_query_restaurants = "SELECT restaurant_id, name FROM restaurants"
    result_restaurants = db.session.execute(text(sql_query_restaurants))
    restaurants = result_restaurants.fetchall()

    return render_template("add_restaurants_to_group.html", groups=groups, restaurants=restaurants)

@app.route("/remove_restaurant_from_group/<int:restaurant_id>/<int:group_id>", methods=["POST"])
def remove_restaurant_from_group(restaurant_id, group_id):
    db.session.execute(text("DELETE FROM group_restaurants WHERE restaurant_id = :restaurant_id AND group_id = :group_id"),
                       {"restaurant_id": restaurant_id, "group_id": group_id})
    db.session.commit()
    return redirect(url_for("edit_groups"))

@app.route("/web_dev_edit_ravintola/<int:restaurant_id>", methods=["GET", "POST"])
def web_dev_edit_ravintola(restaurant_id):
    if request.method == "GET":
        sql_query = "SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"
        result = db.session.execute(text(sql_query), {"restaurant_id": restaurant_id})
        restaurant = result.fetchone()

        if restaurant is None:
            return "Restaurant not found", 404

        sql_groups = "SELECT group_id, group_name FROM groups"
        groups_result = db.session.execute(text(sql_groups))
        groups = groups_result.fetchall()

        sql_assigned_groups = """
            SELECT g.group_id
            FROM groups g
            JOIN group_restaurants gr ON g.group_id = gr.group_id
            WHERE gr.restaurant_id = :restaurant_id
        """
        assigned_result = db.session.execute(text(sql_assigned_groups), {"restaurant_id": restaurant_id})
        restaurant_groups = [row.group_id for row in assigned_result.fetchall()]

        return render_template("web_dev_edit_ravintola.html", restaurant=restaurant, groups=groups, restaurant_groups=restaurant_groups, restaurant_id=restaurant_id)

    if request.method == "POST":
        description = request.form["description"]
        opening_hours = request.form["opening_hours"]
        selected_groups = request.form.getlist("groups")

        sql_update = """UPDATE restaurants 
                        SET description = :description, opening_hours = :opening_hours 
                        WHERE restaurant_id = :restaurant_id"""
        db.session.execute(text(sql_update), {
            "description": description,
            "opening_hours": opening_hours,
            "restaurant_id": restaurant_id
        })
        
        db.session.execute(text("DELETE FROM group_restaurants WHERE restaurant_id = :restaurant_id"), {"restaurant_id": restaurant_id})
        
        for group_id in selected_groups:
            db.session.execute(text("INSERT INTO group_restaurants (restaurant_id, group_id) VALUES (:restaurant_id, :group_id)"),
                               {"restaurant_id": restaurant_id, "group_id": group_id})

        db.session.commit()
        return redirect(url_for("web_dev_page"))
    
@app.route("/update_restaurant/<int:restaurant_id>", methods=["POST"])
def update_restaurant(restaurant_id):
    description = request.form["description"]
    opening_hours = request.form["opening_hours"]

    sql_update = """UPDATE restaurants 
                    SET description = :description, opening_hours = :opening_hours 
                    WHERE restaurant_id = :restaurant_id"""
    db.session.execute(text(sql_update), {
        "description": description,
        "opening_hours": opening_hours,
        "restaurant_id": restaurant_id
    })
    db.session.commit()

    return redirect(url_for("web_dev_page"))

@app.route("/remove_restaurant/<int:restaurant_id>", methods=["POST"])
def remove_restaurant(restaurant_id):
    db.session.execute(text("DELETE FROM review WHERE restaurant_id = :restaurant_id"), {"restaurant_id": restaurant_id})
    db.session.execute(text("DELETE FROM restaurants WHERE restaurant_id = :restaurant_id"), {"restaurant_id": restaurant_id})
    db.session.commit()
    
    return redirect(url_for("web_dev_page"))

@app.route("/web_dev_add_review")
def web_dev_add_review():
    sql_query = "SELECT restaurant_id, name FROM restaurants"
    result = db.session.execute(text(sql_query))
    restaurants = result.fetchall()
    
    return render_template("web_dev_add_review.html", restaurants=restaurants)

@app.route("/remove_review/<int:review_id>", methods=["POST"])
def remove_review(review_id):
    if not is_admin():
        return "Unauthorized", 403

    restaurant_id = request.form.get("restaurant_id")
    db.session.execute(text("DELETE FROM review WHERE review_id = :review_id"), {"review_id": review_id})
    db.session.commit()

    return redirect(url_for("web_dev_review", restaurant_id=restaurant_id))

@app.route("/submit_web_dev_review", methods=["POST"])
def submit_web_dev_review():
    if "username" in session:
        username = session["username"]

        sql_account_id = "SELECT account_id FROM accounts WHERE username=:username"
        result = db.session.execute(text(sql_account_id), {"username": username})
        account = result.fetchone()
        
        if account:
            account_id = account.account_id
            rating = request.form["rating"]
            comment = request.form["comment"] or "-"
            restaurant_id = request.form["restaurant_id"]

            sql_insert = """INSERT INTO review (account_id, restaurant_id, rating, comment) 
                            VALUES (:account_id, :restaurant_id, :rating, :comment)"""
            db.session.execute(text(sql_insert), {
                "account_id": account_id,
                "restaurant_id": restaurant_id,
                "rating": rating,
                "comment": comment
            })
            db.session.commit()
            return redirect(url_for("web_dev_review", restaurant_id=restaurant_id))

@app.route("/web_dev_review/<int:restaurant_id>")
def web_dev_review(restaurant_id):
    sql_query = """SELECT r.review_id, r.rating, r.comment, a.username 
                   FROM review r JOIN accounts a ON r.account_id = a.account_id 
                   WHERE r.restaurant_id = :restaurant_id"""
    result = db.session.execute(text(sql_query), {"restaurant_id": restaurant_id})
    reviews = result.fetchall()

    sql_restaurant = "SELECT name FROM restaurants WHERE restaurant_id = :restaurant_id"
    restaurant_result = db.session.execute(text(sql_restaurant), {"restaurant_id": restaurant_id})
    restaurant = restaurant_result.fetchone()

    return render_template("web_dev_review.html", reviews=reviews, restaurant=restaurant, restaurant_id=restaurant_id)

@app.route("/add_review")
def add_review():
    sql_query = "SELECT restaurant_id, name FROM restaurants"
    result = db.session.execute(text(sql_query))
    restaurants = result.fetchall()
    
    return render_template("add_review.html", restaurants=restaurants)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    if "username" in session:
        username = session["username"]

        sql_account_id = "SELECT account_id FROM accounts WHERE username=:username"
        result = db.session.execute(text(sql_account_id), {"username": username})
        account = result.fetchone()
        
        if account:
            account_id = account.account_id
            rating = request.form["rating"]
            comment = request.form["comment"] or "-"
            restaurant_id = request.form["restaurant_id"]

            if len(comment) > 52:
                comment = comment[:52]

            sql_insert = """INSERT INTO review (account_id, restaurant_id, rating, comment) VALUES (:account_id, :restaurant_id, :rating, :comment)"""
            db.session.execute(text(sql_insert), {
                "account_id": account_id,
                "restaurant_id": restaurant_id,
                "rating": rating,
                "comment": comment
            })
            db.session.commit()
            return redirect(url_for("restaurants"))

@app.route("/reviews/<int:restaurant_id>")
def reviews(restaurant_id):
    #testing
    sql_query = """SELECT r.rating, r.comment, a.username FROM review r JOIN accounts a ON r.account_id = a.account_id WHERE r.restaurant_id = :restaurant_id"""
    result = db.session.execute(text(sql_query), {"restaurant_id": restaurant_id})
    reviews = result.fetchall()

    sql_restaurant = "SELECT name FROM restaurants WHERE restaurant_id = :restaurant_id"
    restaurant_result = db.session.execute(text(sql_restaurant), {"restaurant_id": restaurant_id})
    restaurant = restaurant_result.fetchone()

    return render_template("reviews.html", reviews=reviews, restaurant=restaurant)