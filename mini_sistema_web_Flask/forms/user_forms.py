# forms/user_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message="El nombre de usuario es obligatorio"),
        Length(min=3, max=80, message="Debe tener entre 3 y 80 caracteres")
    ])
    email = StringField('Correo electrónico', validators=[
        DataRequired(message="El correo es obligatorio"),
        Email(message="Correo inválido"),
        Length(max=120)
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria"),
        Length(min=6, message="Mínimo 6 caracteres")
    ])
    confirm_password = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message="Confirma tu contraseña"),
        EqualTo('password', message="Las contraseñas no coinciden")
    ])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[
        DataRequired(message="El correo es obligatorio"),
        Email(message="Correo inválido")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria")
    ])
    submit = SubmitField('Iniciar sesión')


class EditProfileForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message="El nombre de usuario es obligatorio"),
        Length(min=3, max=80)
    ])
    email = StringField('Correo electrónico', validators=[
        DataRequired(message="El correo es obligatorio"),
        Email(message="Correo inválido")
    ])
    password = PasswordField('Nueva contraseña (opcional)', validators=[
        Optional(),
        Length(min=6, message="Mínimo 6 caracteres")
    ])
    submit = SubmitField('Guardar cambios')