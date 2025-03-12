import os
from flask import Flask, flash, redirect, url_for, render_template, send_file, request, session, abort
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from error_handlers import error_handlers
from datetime import datetime
import pytz  # Add this import at the top of the file

app = Flask(__name__)

#---- APP CONFIGURATION ----
app.config.from_pyfile('etc/defaults.cfg')

# Initialize extensions after loading config
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)  # Move this here, after loading config

# Register error handlers
error_handlers(app)

app.permanent_session_lifetime = timedelta(minutes=15)

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

#---- ROUTING AND PAGES ----

@app.route("/terms")
def home2():
    return render_template("terms.html", username=session.get("email"))

@app.route("/contacts")
def contacts():
    return render_template("contacts.html", username=session.get("email"))

@app.route("/history")
def history():
    return render_template("history.html", username=session.get("email"))

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
            # Handle multiple product deletion
            if 'product_ids[]' in request.form:
                product_ids = request.form.getlist('product_ids[]')
                product_names = request.form.getlist('product_names[]')
                product_image_urls = request.form.getlist('product_image_urls[]')
                
                deleted_count = 0
                for i in range(len(product_ids)):
                    product_to_delete = Products.query.filter_by(id=product_ids[i], name=product_names[i]).first()
                    if product_to_delete:
                        # Delete the product from db
                        db.session.delete(product_to_delete)
                        # Delete the product image from filesystem
                        try:
                            os.remove(product_image_urls[i])
                        except OSError:
                            # If file doesn't exist, continue with deletion
                            pass
                        deleted_count += 1
                
                db.session.commit()
                if deleted_count > 0:
                    flash(f"{deleted_count} product{'s' if deleted_count > 1 else ''} deleted successfully", "success")
                else:
                    flash("No products were deleted", "error")
                return redirect(url_for("inventory"))
            
            # Handle single product deletion
            elif 'product_id' in request.form:
                product_id = request.form["product_id"]
                product_name = request.form["product_name"]
                product_to_delete = Products.query.filter_by(id=product_id, name=product_name).first()
                if product_to_delete:
                    # Delete the product from db
                    db.session.delete(product_to_delete)
                    db.session.commit()
                    # Delete the product from filesystem
                    try:
                        os.remove(request.form["product_image_url"])
                    except OSError:
                        # If file doesn't exist, continue
                        pass
                    flash(f"'{product_name}' deleted successfully", "success")
                else:
                    flash('Product to delete not found', 'error')
                return redirect(url_for("inventory"))
            
            # Handle product addition
            else:
                uploaded_file = request.files['file']
                filename = uploaded_file.filename
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                        flash("You attempted to insert a non compatible file. Please upload a JPEG or PNG file", "info")
                        return redirect(url_for("inventory"))
                    # Check if product is already existing before adding it
                    product_name = request.form["product_name"]
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

        # Handle sorting parameters
        sort_column = request.args.get('sort', 'date')
        sort_order = request.args.get('order', 'desc')

        # Validate sort_column against Products model
        valid_columns = ['id', 'name', 'category', 'date']
        if sort_column not in valid_columns:
            sort_column = 'id'

        # Determine the order direction
        if sort_order == 'asc':
            order = getattr(Products, sort_column).asc()
        else:
            order = getattr(Products, sort_column).desc()

        # Fetch sorted products
        products = Products.query.order_by(order).all()

        return render_template("inventory.html", 
                             values=products,
                             current_sort=sort_column,
                             current_order=sort_order)
    
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

# Website homepage
@app.route("/homepage")
@app.route("/home")
@app.route("/index")
@app.route("/")
def home():
    if "email" in session:
        if session["email"] == app.config['ADMIN_EMAIL']:
            return render_template("index.html", username=session["email"], is_admin=True)
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
    chosen_category = session.get("last_category", "marble")
    
    if request.method == "POST":
        if "product_name" in request.form:
            old_product_name = request.form["product_name"]
            retrived_category = Products.query.filter_by(name=old_product_name).first()
            chosen_category = retrived_category.category
        else:
            chosen_category = request.form["category"]
        session["last_category"] = chosen_category

    filters = request.args.getlist('filters')
    current_page = request.args.get('page', 1, type=int)
    
    # Get only tags that are used by products in the current category
    available_tags = Tags.query.join(Tags.products).filter(
        Products.category == chosen_category.lower()
    ).distinct().all()
    
    query = Products.query.filter_by(category=chosen_category.lower())
    if filters:
        query = query.join(Products.tags).filter(Tags.name.in_(filters))
    
    pagination = query.paginate(page=current_page, per_page=27, error_out=False)
    products = pagination.items

    if "email" in session:
        return render_template("collections.html", chosen_category=chosen_category, products=products, 
                            pagination=pagination, username=session["email"], filters=filters, tags=available_tags)
    else:
        return render_template("collections.html", chosen_category=chosen_category, products=products, 
                            pagination=pagination, filters=filters, tags=available_tags)

@app.route("/product", methods=["POST", "GET"])
def product():
    if request.method == "POST":
        chosen_product_url = request.form["product_image_url"]
        chosen_product_name = request.form["product_name"]
        chosen_product_category = request.form["product_category"]
        if "email" in session:
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
            # Fetch product images for each item in basket
            basket_data = session["basket_data"]
            for item in basket_data:
                product = Products.query.filter_by(name=item['product_name']).first()
                if product:
                    item['image_url'] = product.image_url
            
            return render_template("basket.html", basket_data=basket_data, username=session["email"])
        return render_template("basket.html")
    
    flash("Please log-in to access this page", "info")
    return redirect(url_for("user"))

@app.route("/submit_order", methods=["POST"])
def submit_order():
    if "email" not in session:
        flash("Please log in to submit your order", "error")
        return redirect(url_for("login"))
    
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        comments = request.form.get('comments', '')
        basket_data = session.get("basket_data", [])
        
        if not basket_data:
            flash("Your basket is empty", "error")
            return redirect(url_for("basket"))

        # Calculate total items
        total_items = sum(item['product_quantity'] for item in basket_data)
        
        # Generate order ID and timestamp in Italian timezone
        italian_tz = pytz.timezone('Europe/Rome')
        timestamp = datetime.now(italian_tz)
        order_id = f"SVE{timestamp.strftime('%Y%m%d%H%M%S')}"

        # Create and send confirmation email to admin
        admin_html = render_template(
            'email/order_confirmation.html',
            name=name,
            email=email,
            phone=phone,
            comments=comments,
            basket_data=basket_data,
            order_id=order_id,  # Add order_id
            timestamp=timestamp  # Add timestamp
        )
        
        admin_msg = Message(
            subject=f"New Order from SVE website - {name}",
            recipients=[app.config['MAIL_RECIPIENT']],
            html=admin_html,
            reply_to=email
        )
        mail.send(admin_msg)

        # Create and send receipt to customer
        customer_html = render_template(
            'email/order_receipt.html',
            name=name,
            email=email,
            phone=phone,
            comments=comments,
            basket_data=basket_data,
            order_id=order_id,
            timestamp=timestamp,
            total_items=total_items
        )
        
        customer_msg = Message(
            subject=f"Your STUDIOSVE Order Confirmation - #{order_id}",
            recipients=[session['email']],
            html=customer_html
        )
        mail.send(customer_msg)
        
        # Clear basket after successful order
        session.pop("basket_data", None)
        flash("Your order has been submitted successfully!", "success")
        return redirect(url_for("home"))
        
    except Exception as e:
        print(f"Error sending email: {e}")
        flash("There was an error submitting your order. Please try again.", "error")
        return redirect(url_for("basket"))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if "email" in session:
            return redirect(url_for("user"))
        
        email = request.form["email"]
        password = request.form["pswd"]
        confirm_password = request.form["confirm_pswd"]

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for("register"))

        # Check if the email is already in use
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already in use. Please choose another email.", "error")
            return redirect(url_for("register"))

        # Check if the password is empty
        if not password:
            flash("Password cannot be empty. Please insert a password.", "error")
            return redirect(url_for("register"))
        
        # If all checks pass, create the new user
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
            return send_file('static/docs/SVEpricelistJAN2025.pdf', as_attachment=False)
        except Exception as e:
            abort(404)  # If the file is not found, return 404 error
    else:
        return redirect(url_for("user"))

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()