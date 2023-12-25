import math

from flask import render_template, request, redirect, jsonify, session
import dao
import utils
from app import app, login
from flask_login import login_user


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    prods = dao.get_products(kw, cate_id, page)

    num = dao.count_product()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html',
                           products=prods, pages=math.ceil(num/page_size))


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)

    return redirect('/admin')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json

    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(data.get("id"))
    if id in cart: # da co trong gio
        cart[id]['quantity'] += 1
    else: # chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": 1
        }

    session['cart'] = cart
    """
    {
        "1": {
            "id": "1",
            "name": "abc",
            "price": 123,
            "quantity": 2
        }, "2": {
            "id": "2",
            "name": "abc",
            "price": 123,
            "quantity": 1
        }
    }
    """

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/login', methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

        next = request.args.get('next')
        return redirect("/" if next is None else next)

    return render_template('login.html')


@app.route("/api/pay", methods=['post'])
def pay():
    if dao.add_receipt(session.get('cart')):
        del session['cart']
        return jsonify({'status': 200})

    return jsonify({'status': 500, 'err_msg': 'Something wrong!'})


@app.context_processor
def common_responses():
    return {
        'categories': dao.get_categories(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
