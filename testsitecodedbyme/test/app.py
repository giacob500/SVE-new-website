from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(50))

# Create a sample database
with app.app_context():
    db.create_all()
    sample_data = [
        Product(name='Product1', category='Category1'),
        Product(name='Product2', category='Category2'),
        # Add more sample data as needed
    ]
    db.session.add_all(sample_data)
    db.session.commit()

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    items_per_page = 10

    # Paginate the query
    products = Product.query.filter_by(category='Category1').paginate(page, per_page=items_per_page)

    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
