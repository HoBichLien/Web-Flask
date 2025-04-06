from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField,SubmitField,PasswordField,FileField
from wtforms.validators import DataRequired, Length,Email,Regexp,ValidationError,Optional
from shop.models.account import Account

class ProfileForm(FlaskForm):
    fullname=StringField(
        "Fullname", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Length(min=6,max=160,message='Nhập từ 6 - 32 ký tự')
        ],
        render_kw={'class':'form-control ','placeholder':'Enter fullname'} #thêm class form-control
    )
    email=StringField(
        "Email", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Email()
        ],
        render_kw={'class':'form-control','placeholder':'Enter email','disabled':'disabled'} 
    )
    password=PasswordField(
        "Password", 
        validators=[
            Optional(), 
            Length(min=6,max=32,message='Nhập từ 6 - 32 ký tự'),
            Regexp('^[a-zA-Z0-9]*$',message='Password chỉ được phép nhập ký tự và số')
        ],
        render_kw={'class':'form-control','placeholder':'Enter Password'} 
    )
    phone=StringField(
        "Phone", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
            Length(min=10,max=12,message='Nhập từ 10 - 12 số'),
            Regexp('^[0-9]*$',message='Phone chỉ được phép nhập số')
        ],
        render_kw={'class':'form-control','placeholder':'Enter Phone'} 
    )
    address=StringField(
        "Address", 
        validators=[
            DataRequired(message='Vui lòng không để trống'),
        ],
        render_kw={'class':'form-control','placeholder':'Enter Address'} 
    )
    image=FileField(
        "Avatar", 
        render_kw={'class':'form-control'} #thêm class form-control
    )
    submit=SubmitField(
        'Update Profile',
        render_kw={'class':'btn btn-primary btn-sm'} 
    )