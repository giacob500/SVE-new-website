from flask import Flask, render_template, request

app = Flask(__name__)

# Dummy data (replace with your actual data)
all_products = [f"Product {i}" for i in range(1, 101)]  # 100 dummy products

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    items_per_page = 10
    start = (page - 1) * items_per_page
    end = start + items_per_page
    products = all_products[start:end]
    return render_template('index.html', products=products, page=page)

if __name__ == '__main__':
    app.run(debug=True)