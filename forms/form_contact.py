from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,Email,Regexp,ValidationError
from shop.models.account import Account

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone', validators=[
        DataRequired(),
        Regexp(r'^\+?\d{7,15}$', message="Invalid phone number."),
        Length(max=15)
    ])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Send Message')
