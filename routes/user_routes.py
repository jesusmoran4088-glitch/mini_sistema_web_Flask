from functools import wraps
from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, session
)
from models import db
from models.user import User
from routes.forms import RegisterForm, LoginForm, EditProfileForm

user_bp = Blueprint("users", __name__)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para acceder.", "warning")
            return redirect(url_for("users.login"))
        return f(*args, **kwargs)
    return wrapper


@user_bp.route("/")
def index():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("user_list.html", users=users)


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("El correo ya está registrado.", "danger")
            return render_template("register.html", form=form)
        if User.query.filter_by(username=form.username.data).first():
            flash("El nombre de usuario ya existe.", "danger")
            return render_template("register.html", form=form)

        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower().strip(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("¡Registro exitoso! Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Bienvenido, {user.username}!", "success")
            return redirect(url_for("users.index"))
        flash("Credenciales inválidas.", "danger")
    return render_template("login.html", form=form)


@user_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("users.index"))


@user_bp.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template("profile.html", user=user)


@user_bp.route("/profile/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    if session.get("user_id") != id:
        flash("No puedes editar el perfil de otro usuario.", "danger")
        return redirect(url_for("users.index"))

    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        exist_email = User.query.filter(
            User.email == form.email.data.lower(), User.id != id
        ).first()
        exist_user = User.query.filter(
            User.username == form.username.data, User.id != id
        ).first()
        if exist_email:
            flash("Ese correo ya está en uso.", "danger")
        elif exist_user:
            flash("Ese nombre de usuario ya está en uso.", "danger")
        else:
            user.username = form.username.data.strip()
            user.email = form.email.data.lower().strip()
            db.session.commit()
            session["username"] = user.username
            flash("Perfil actualizado correctamente.", "success")
            return redirect(url_for("users.profile", id=user.id))
    return render_template("edit_profile.html", form=form, user=user)


@user_bp.route("/profile/<int:id>/delete", methods=["POST"])
@login_required
def delete_profile(id):
    user = User.query.get_or_404(id)
    if session.get("user_id") != id:
        flash("No puedes eliminar a otro usuario.", "danger")
        return redirect(url_for("users.index"))
    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash("Usuario eliminado correctamente.", "info")
    return redirect(url_for("users.index"))