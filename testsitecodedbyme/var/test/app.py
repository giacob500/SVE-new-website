"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Create some dummy data
with app.app_context():
    db.create_all()
    for i in range(1, 101):
        db.session.add(Product(name=f"Product {i}"))
    db.session.commit()

@app.route('/')
def index():
    # Pagination setup
    page, per_page, offset = get_page_args()
    per_page = 10
    total = Product.query.count()
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    # Query for products for the current page
    products = Product.query.offset(offset).limit(per_page).all()

    return render_template('index.html', products=products, pagination=pagination)

@app.route('/phone')
def phone():
    return render_template('phone_number.html')

if __name__ == '__main__':
    app.run(debug=True)
"""