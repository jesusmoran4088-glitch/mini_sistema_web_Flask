from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class RegisterForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=80, message="Entre 3 y 80 caracteres."),
            Regexp(r"^[A-Za-z0-9_]+$", message="Solo letras, números y guiones bajos.")
        ],
    )
    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Formato de correo inválido."),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=6, message="Mínimo 6 caracteres."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Confirma la contraseña."),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
    )
    submit = SubmitField("Registrarse")


class LoginForm(FlaskForm):
    email = StringField(
        "Correo electrónico",
        validators=[DataRequired(), Email(message="Correo inválido.")],
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), Length(min=6)],
    )
    submit = SubmitField("Iniciar sesión")


class EditProfileForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = StringField(
        "Correo electrónico",
        validators=[DataRequired(), Email(message="Correo inválido.")],
    )
    submit = SubmitField("Guardar cambios")