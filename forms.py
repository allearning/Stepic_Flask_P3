import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email, Regexp

PHONE_RE = r"^((\+\d)|\d)?\-?(\([\d]+\))?\-?[\d\-]+[\d]$"


def password_check(form, field):
    msg = "Пароль должен содержать латинские сивмолы в верхнем и нижнем регистре и цифры"
    patern1 = re.compile('[a-z]+')
    patern2 = re.compile('[A-Z]+')
    patern3 = re.compile('\d+')
    if (not patern1.search(field.data) or
            not patern2.search(field.data) or
            not patern3.search(field.data)):
        raise ValidationError(msg)


class LoginForm(FlaskForm):
    username = StringField("Имя:", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField(
        "Имя:",
        validators=[
            DataRequired(),
            Email("Нужно указать электронную почту в качестве имени"),
            Length(min=4, max=32, message="Имя должно быть не менее 4 и не боле 32 символов"),
        ]
    )
    password = PasswordField(
        "Пароль:",
        validators=[
            DataRequired(),
            Length(min=8, message="Пароль должен быть не менее 8 символов"),
            EqualTo('confirm_password', message="Пароли не одинаковые"),
            password_check
        ]
    )
    confirm_password = PasswordField("Пароль ещё раз:")
    submit = SubmitField('Зарегистрироваться')


class CartForm(FlaskForm):
    username = StringField("Ваше имя", validators=[DataRequired()])
    address = StringField("Адрес", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    phone = StringField("Телефон",
                        validators=[DataRequired(), Regexp(PHONE_RE, message="Номер телефона не номер телефона")])
    submit = SubmitField('Оформить заказ')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        "Пароль:",
        validators=[
            DataRequired(),
            Length(min=8, message="Пароль должен быть не менее 8 символов"),
            EqualTo('confirm_password', message="Пароли не одинаковые"),
            password_check
        ]
    )
    confirm_password = PasswordField("Пароль ещё раз:")
