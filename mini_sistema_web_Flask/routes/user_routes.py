# routes/user_routes.py
from functools import wraps
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, session)
from models import db
from models.user import User
from forms.user_forms import RegisterForm, LoginForm, EditProfileForm

user_bp = Blueprint('user', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder.', 'error')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Ese correo ya está registrado.', 'error')
            return render_template('register.html', form=form)
        if User.query.filter_by(username=form.username.data).first():
            flash('Ese nombre de usuario ya existe.', 'error')
            return render_template('register.html', form=form)

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(f'¡Usuario {user.username} registrado con éxito!', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Bienvenido, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas.', 'error')
    return render_template('login.html', form=form)


@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('index'))


@user_bp.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)


@user_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    if session.get('user_id') != user.id:
        flash('No tienes permiso para editar este perfil.', 'error')
        return redirect(url_for('index'))

    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('user.profile', id=user.id))

    return render_template('edit_profile.html', form=form, user=user)


@user_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_profile(id):
    user = User.query.get_or_404(id)
    if session.get('user_id') != user.id:
        flash('No tienes permiso para eliminar este perfil.', 'error')
        return redirect(url_for('index'))

    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('index'))