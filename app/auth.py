from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .database import db
from .models import User


def register_auth(app):

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if current_user.is_authenticated:
            return redirect(url_for("home"))

        if request.method == "POST":

            username = request.form["username"].strip()

            email = request.form["email"].strip().lower()

            password = request.form["password"]

            if User.query.filter_by(username=username).first():
                flash("اسم المستخدم مستخدم بالفعل.")
                return redirect(url_for("register"))

            if User.query.filter_by(email=email).first():
                flash("البريد الإلكتروني مستخدم بالفعل.")
                return redirect(url_for("register"))

            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )

            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect(url_for("home"))

        return render_template("register.html")


    @app.route("/login", methods=["GET", "POST"])
    def login():

        if current_user.is_authenticated:
            return redirect(url_for("home"))

        if request.method == "POST":

            email = request.form["email"].strip().lower()

            password = request.form["password"]

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(
                user.password_hash,
                password
            ):

                login_user(user)

                return redirect(url_for("home"))

            flash("البريد الإلكتروني أو كلمة المرور غير صحيحة.")

        return render_template("login.html")


    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        return redirect(url_for("home"))

