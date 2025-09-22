from app import db
from flask import render_template, flash, redirect, url_for, request
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from urllib.parse import urlparse
import sqlalchemy as sa
from app.auth import bp



@bp.route("/")
@bp.route("auth/index")
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",title = "Home", posts = posts)

@bp.route("/login",methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username==form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash("invalid password or username")
            return redirect(url_for("auth.login"))
        login_user(user,remember = form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("auth.index")
        return redirect(next_page)
    return render_template("auth/login.html",title = "Sign in", form = form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.index"))

@bp.route("/register", methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("congratz on registration dude, you may sign in")
        return redirect(url_for("auth.index"))
    return render_template("auth/register.html", title = "Register",form = form)