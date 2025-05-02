from flask import render_template, request, redirect, url_for, session, jsonify
from SaleApp import app, login
import utils
import math
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from SaleApp.admin import *
from SaleApp.models import UserRole


@app.route("/")
def home():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)

    products = utils.load_products(cate_id=cate_id, kw=kw, page=page)
    counter = utils.count_products()

    return render_template("index.html",
                           products=products,
                           pages = math.ceil(counter / app.config['PAGE_SIZE']),
                           page=page)


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = "Password does NOT match!!!"
        except Exception as e:
            err_msg = "Error: " + str(e)

    return render_template('register.html', err_msg=err_msg)



@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            user = utils.check_login(username=username, password=password)
            if user:
                login_user(user=user)

                next = request.args.get('next', 'home')
                return redirect(url_for(next))
            else:
                err_msg = 'Username or Password is Incorrect!!!'

        except Exception as ex:
            err_msg = str(ex)

    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


@app.route("/products")
def products_list():
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    products = utils.load_products(cate_id=cate_id,
                                   kw=kw,
                                   from_price=from_price,
                                   to_price=to_price)

    return render_template('products.html', products=products)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    page = request.args.get('page', 1, type=int)
    product = utils.get_product_by_id(product_id)
    comments = utils.get_comments(product_id=product_id , page=page)

    return render_template('product_detail.html',
                           comments=comments,
                           product=product,
                           page=page,
                           pages=math.ceil(utils.count_comment(product_id=product_id) / app.config['COMMENT_SIZE']))


@app.route('/cart')
def cart():
    return render_template('cart.html',
                           stats=utils.count_cart(session.get('cart')))


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')


    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/update-cart', methods=['PUT'])
def update_cart():
    data = request.get_json()
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/app/delete-cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        del cart[product_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))



@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        session.pop('cart', None)
        return jsonify({'code': 200, 'message': 'Payment successful'})
    except Exception as ex:
        return jsonify({'code': 400, 'message': f'Error: {str(ex)}'})


@app.route('/api/comments', methods=['POST'])
@login_required
def add_comment():
    data = request.get_json()
    content = data.get('content')
    product_id = data.get('product_id')

    try:
        comment = utils.add_comment(content=content, product_id=product_id)
    except Exception as e:
        return {'status': 404, 'err_msg': e}

    return {'status': 201, 'comment': {
        'id': comment.id,
        'content': comment.content,
        'created_date': comment.created_date,
        'user': {
            'username': current_user.username,
            'avatar': current_user.avatar or url_for('static', filename='images/default-avatar.jpg')
        }
    }}


@app.route('/comments/<int:product_id>')
def load_comments(product_id):
    page = request.args.get('page', 1, type=int)
    comments = utils.get_comments(product_id=product_id, page=page)
    pages = math.ceil(utils.count_comment(product_id=product_id) / app.config['COMMENT_SIZE'])

    return render_template('partials/_comment.html',
                           comments=comments,
                           page=page,
                           pages=pages,
                           product_id=product_id)


if __name__=='__main__':
    app.run(debug=True)



