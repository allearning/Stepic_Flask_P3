import json
from datetime import datetime
from functools import wraps

from flask import abort, session, redirect, request, render_template
from sqlalchemy import func

from app import app, db
from forms import LoginForm, RegistrationForm, CartForm
from models import User, Category, Item, Order


# from forms import LoginForm, RegistrationForm, ChangePasswordForm


# ------------------------------------------------------
# Декораторы авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("login_required")
        if not session.get('user'):
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("admin_only")
        if session.get('user')["role"] != "admin":
            abort(403, description="Вам сюда нельзя")
        return f(*args, **kwargs)

    return decorated_function


# ------------------------------------------------------
@app.route('/')
def render_index():
    categories = db.session.query(Category).all()
    items = {}
    for category in categories:
        items[category.id] = db.session.query(Item).filter(Item.category_id == category.id).order_by(
            func.random()).limit(3)

    output = render_template("main.html", categories=categories, items=items)
    return output


@app.route('/register/', methods=["GET", "POST"])
def render_register():
    form = RegistrationForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("register.html", form=form)
        if db.session.query(User).filter(User.name == form.username.data):
            form.username.errors.append("Такое имя пользователя уже занято")
            return render_template("register.html", form=form)
        user = User(name=form.username.data)
        user.password = form.password.data
        user.role = "admin"
        db.session.add(user)
        db.session.commit()
        return redirect("/auth/")

    return render_template("register.html", form=form)


@app.route('/login/', methods=["GET"])
def render_login():
    return redirect("/auth")


@app.route('/auth/', methods=["GET", "POST"])
def render_auth():
    if session.get("user"):
        return redirect("/")

    form = LoginForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("auth.html", form=form)

        user = User.query.filter_by(name=form.username.data).first()
        if user and user.password_valid(form.password.data):
            session["user"] = {
                "id": user.id,
                "username": user.name,
                "role": user.role,
            }

            return redirect("/account/")

        form.username.errors.append("Не верное имя или пароль")

    return render_template("auth.html", form=form)


@app.route('/account/', methods=["GET"])
def render_account():
    if not session.get("user"):
        return redirect("/auth/")
    orders = db.session.query(Order).filter(Order.user_id == session.get("user")["id"]).all()

    return render_template("account.html", orders=orders)


@app.route('/logout/', methods=["POST"])
@login_required
def render_logout():
    session.pop("user")
    return redirect("/")


@app.route('/add_item/<item_id>/<int:item_count>', methods=["POST"])
def add_item(item_id, item_count):
    cart = session.get("cart", {})
    if item_id in cart:
        cart[item_id]["count"] += item_count
    else:
        cart[item_id] = {}
        cart[item_id]["count"] = item_count

    item = db.session.query(Item).get(item_id)
    cart[item_id]["price"] = item.price
    cart[item_id]["title"] = item.title
    session["cart"] = cart
    return redirect("/cart/")


@app.route('/remove_item/<item_id>/', methods=["GET"])
def remove_item(item_id):
    cart = session.get("cart", {})
    if item_id in cart:
        del cart[item_id]
    session["cart"] = cart
    session["deleted"] = True
    return redirect("/cart/")


@app.route('/cart/', methods=["GET", "POST"])
def render_cart():
    form = CartForm()
    if request.method == "POST":
        if not session.get("user"):
            return redirect("/auth/")

        if not form.validate_on_submit():
            return render_template("cart.html", form=form)

        if not session.get("cart", {}):
            form.submit.errors.append("Корзина не должна быть пустой")
            return render_template("cart.html", form=form)

        order = Order(user_id=session.get("user")["id"], status='Размещен', date=datetime.today(),
                      email=form.email.data)
        order.items = json.dumps(session.get("cart"))

        db.session.add(order)
        db.session.commit()
        session.pop("cart")
        session.pop("total_cost")
        session.pop("total_count")

        return render_template("ordered.html")

    session["total_cost"] = sum([item["price"] * item["count"] for item in session.get("cart", {}).values()])
    session["total_count"] = len(session.get("cart", {}))
    output = render_template("cart.html", form=form, deleted=session.get("deleted"),
                             total_cost=session.get("total_cost", 0),
                             total_count=session.get("total_count", 0))
    session["deleted"] = False
    return output
