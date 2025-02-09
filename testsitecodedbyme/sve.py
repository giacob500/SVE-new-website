import os
from flask import Flask, flash, redirect, url_for, render_template, send_file, request, session, abort
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#---- APP CONFIGURATION ----

app.config.from_pyfile('etc/defaults.cfg')

app.permanent_session_lifetime = timedelta(minutes=15)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#---- DATABASE CONFIGURATION ----

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    units = db.Column(db.Integer)
    price = db.Column(db.Integer)
    date = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    # Add relationship to tags
    tags = db.relationship('Tags', secondary='product_tags', backref=db.backref('products', lazy='dynamic'))

# Association table for products and tags
product_tags = db.Table('product_tags',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

""" #---- ERROR HANDLING ----

# Error handler for client error 404
@app.errorhandler(404)
def invalid_route(e):
    return render_template("error.html", error_message="The source you are looking forward does not exist. Please return to the homepage."), 404

# Error handler for all server errors (5xx)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", error_message="Internal Server Error"), 500


# Error handler for all other errors
@app.errorhandler(Exception)
def handle_all_errors(e):
    return render_template('error.html', error_message='An unexpected error occurred'), 500
 """

#---- ROUTING AND PAGES ----

@app.route("/terms")
def home2():
    return render_template("terms.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@app.route("/history")
def history():
    return render_template("history.html")

# Pages accessible only to website admins (currently just lorenzi@lorenzi.net) to check all users currently registered on website
@app.route("/admin")
def adminview():
    if "email" in session and session["email"] == app.config['ADMIN_EMAIL']:
        return render_template("admin_view.html", values=Users.query.all())
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))
    
@app.route("/inventory", methods=['GET', 'POST'])
def inventory():
    if "email" in session and session["email"] == app.config['ADMIN_EMAIL']:
        if request.method == 'POST':
            product_name = request.form["product_name"]
            if 'product_id' in request.form:
                product_id = request.form["product_id"]
                product_to_delete = Products.query.filter_by(id=product_id, name=product_name).first()
                if product_to_delete:
                    # Delete the product from db
                    db.session.delete(product_to_delete)
                    db.session.commit()
                    # Delete the product from filesystem
                    os.remove(request.form["product_image_url"])
                    flash(f"'{product_name}' deleted successfully", "success")
                else:
                    flash('Product to delete not found', 'error')
            else:
                uploaded_file = request.files['file']
                filename = uploaded_file.filename
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                        flash("You attempted to insert a non compatible file. Please upload a JPEG or PNG file", "info")
                        return redirect(url_for("inventory"))
                    # Check if product is already existing before adding it
                    product_category = request.form["product_category"]
                    
                    check = Products.query.filter_by(name=product_name, category=product_category).first()
                    if check is None:
                        # Upload image in correct folder based on product category
                        retrived_category = Products.query.filter_by(category=product_category).first()
                        temporary_path = app.config['UPLOAD_PATH'] + "/" + retrived_category.category
                        uploaded_file.save(os.path.join(temporary_path, filename))
                        
                        new_product = Products(name=product_name, category=product_category, image_url=temporary_path + "/" + filename)
                        db.session.add(new_product)
                        db.session.commit()
                        flash(f"'{product_name}' added successfully", "success")
                    else:
                        flash("You attempted to insert a product that already exist", "error")
                
            return redirect(url_for("inventory"))


        return render_template("inventory.html", values=Products.query.all())
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

# Website homepage
@app.route("/homepage")
@app.route("/home")
@app.route("/index")
@app.route("/")
def home():
    if "email" in session:
        return render_template("index.html", username=session["email"])
    return render_template("index.html")

@app.route("/categories", methods=["POST", "GET"])
def categories():
    if request.method == "POST":
        
        # If no tile selection has been made in product page, include the whole set in the basket
        product_name = request.form["product_name"]
        if "product_counter" in request.form and "product_type" in request.form:
            product_type = request.form["product_type"]
            if request.form["product_counter"] == "":
                product_counter = 4
                selected_tiles = "Tile A, Tile B, Tile C, Tile D"
            else:
                product_counter = int(request.form["product_counter"])
                selected_tiles = request.form["selected_tiles"]

        product_quantity = int(request.form["product_quantity"])
        
        # Store the data in the session
        product_data = {
                "product_name": product_name,
                "product_quantity": product_quantity,
            }
        if "selected_tiles" in request.form:
            product_data.update({
                "selected_tiles": request.form["selected_tiles"],
            })
        if "product_counter" in request.form and "product_type" in request.form:
            product_data.update({
                "selected_tiles": selected_tiles,
                "product_type": product_type,
                "product_counter": product_counter,
            })
            if "additional_feature" in request.form:
                product_data.update({
                "product_type": product_type + " + " + request.form["additional_feature"],
            })
        else:
            product_data.update({
                "product_type": "N/A",
                "product_counter": "N/A",
                "selected_tiles": "N/A",
            })
        
        # Check if the "product_data" list is already in the session, if not, initialize it
        if "basket_data" not in session:
            session["basket_data"] = []
        session["basket_data"].append(product_data)
        
        if "email" in session:
            return redirect(url_for("categories"))
        else:
            flash("Please log-in to add item to basket", "info")
            return redirect(url_for("user"))
    if "email" in session:
        return render_template("categories.html", username=session["email"])
    else:
        # Redirect to login
        return redirect(url_for("user"))

@app.route("/collections", methods=["POST", "GET"])
def collections():
    if request.method == "POST":
        if "product_name" in request.form:
            # Enter this condition if browsing back from product page
            old_product_name = request.form["product_name"]
            retrived_category = Products.query.filter_by(name=old_product_name).first()
            chosen_category = retrived_category.category
        else:
            chosen_category = request.form["category"]
        session["last_category"] = chosen_category

    # Pagination
    elif request.method == "GET":
        if "last_category" not in session:
            chosen_category = "marble"
        else:
            chosen_category = session["last_category"]
    
    current_page = request.args.get('page', 1, type=int)
    print(type(session["last_category"]))
    items_per_page = 27
    if "items_per_page" in request.args:
        items_per_page = int(request.args.get("items_per_page"))
        session["items_per_page"] = items_per_page
    else:
        if "items_per_page" in session:
            items_per_page = session["items_per_page"]
    pagination = Products.query.filter_by(category=chosen_category.lower()).paginate(page=current_page, per_page=items_per_page, error_out=False)
    products = pagination.items

    # Prevent user tampering page value in the URL
    if "email" in session:
        return render_template("collections.html", chosen_category=chosen_category, products=products, pagination=pagination, username=session["email"])
    else:
        return render_template("collections.html", chosen_category=chosen_category, products=products, pagination=pagination)
    

@app.route("/product", methods=["POST", "GET"])
def product():
    if request.method == "POST":
        chosen_product_url = request.form["product_image_url"]
        chosen_product_name = request.form["product_name"]
        chosen_product_category = request.form["product_category"]
        if "email" in session:

            # Build logic to get product tags and display them
            product = Products.query.filter_by(name=chosen_product_name).first()
            if product:
                product_tags = [tag.name for tag in product.tags]
                print(f"Tags for product '{chosen_product_name}':", product_tags)
            
            return render_template("product.html", chosen_product_url=chosen_product_url, chosen_product_name=chosen_product_name, chosen_product_category=chosen_product_category, username=session["email"])
        else:
            return render_template("product.html", chosen_product_url=chosen_product_url, chosen_product_name=chosen_product_name, chosen_product_category=chosen_product_category)
    return redirect(url_for("user"))
        

@app.route("/basket", methods=["POST", "GET"])
def basket():
    if "email" in session:
        if request.method == "POST":
            #Empty basket
            if "reset" in request.form:
                session.pop("basket_data", None)
            #Delete single element from basket
            elif "remove" in request.form:
                to_remove = request.form["remove"]
                substrings = to_remove.split("; ")
                matching_item = None
                for item in session.get("basket_data", []):
                    if (
                        str(item.get("product_name")) == substrings[0]
                        and str(item.get("product_type")) == substrings[1]
                        and str(item.get("product_counter")) == substrings[2]
                        and str(item.get("selected_tiles")) == substrings[3]
                        and str(item.get("product_quantity")) == substrings[4]
                    ):
                        matching_item = item
                        break

                print(matching_item)
                for item in session.get("basket_data", []):
                    print(item)

                if matching_item:
                    session["basket_data"].remove(matching_item)
            return redirect(url_for("basket"))
        
        if "basket_data" in session:
            return render_template("basket.html", basket_data=session["basket_data"], username=session["email"])
        return render_template("basket.html")
    
    flash("Please log-in to access this page", "info")
    return redirect(url_for("user"))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if "email" in session:
            return redirect(url_for("user"))
        
        email = request.form["email"]
        password = request.form["pswd"]

        # Check if the email is already in use
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already in use. Please choose another email.", "error")
            return redirect(url_for("register"))
        # Check if the password is empty
        if not password:
            flash("Password cannot be empty. Please insert a password.", "error")
            return redirect(url_for("register"))
        
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = Users(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True 
        email = request.form["email"]
        password = request.form["pswd"]

        # Check if there is any corresponding email in db
        found_user = Users.query.filter_by(email=email).first()
        if found_user and bcrypt.check_password_hash(found_user.password, password):
            # Login successful
            session["email"] = found_user.email
            return redirect(url_for("user"))
        else:
            flash("Login Failed, please check email and password.", "error")
        return render_template("login.html")
    
    # If there is already an email in the session check who they are
    if "email" in session:
        return redirect(url_for("user"))
    return render_template("login.html")
    
# Check if user is already logged in, otherwise prompt login screen
@app.route("/user")
def user():
    # If there is already an email in the session and it corresponds to an email in the db
    if "email" in session and Users.query.filter_by(email=session["email"]).first():
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    # Clear session related data
    session.pop("email", None)
    session.pop("_flashes", None)
    session.pop("basket_data", None)
    return redirect(url_for("home"))

@app.route("/pricing")
def pricing():
    if "email" in session: 
        try:
            # Path to the PDF you want to serve
            return send_file('static/docs/SVEpricelistJan2024.pdf', as_attachment=False)
        except Exception as e:
            abort(404)  # If the file is not found, return 404 error
    else:
        return redirect(url_for("user"))

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()