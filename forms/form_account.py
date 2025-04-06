from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SelectField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,Email,Regexp,ValidationError
from shop.models.account import Account


class RegisterForm(FlaskForm):
    fullname=StringField(
        "Fullname",
          validators=[DataRequired(),Length(min=6,max=160,message="Fullname chỉ dược phép nhập từ 6 đến 160 kí tự")],
          render_kw={'class':'form-control',"placeholder":"Enter fullname"}
    )
    email=StringField(
        "Email",
          validators=[DataRequired(),Email()],
          render_kw={'class':'form-control',"placeholder":"Enter email"}
    )
    password=PasswordField(
        "Password",
          validators=[DataRequired(),Length(min=6,max=32,message="Password chỉ nhập từ 6-32 kí tự"),
                      Regexp('^[a-zA-Z0-9]*$',message="Password chỉ dược phép nhập kí tự và số")],
          render_kw={'class':'form-control',"placeholder":"Enter Password"}
    )
    phone=StringField(
        "Phone Number",
          validators=[DataRequired(),Length(min=10,max=12,message="Phone chỉ nhập từ 10-12 kí tự"),
                      Regexp('^[0-9]*$',message="Phone chỉ dược phép nhập số")],
          render_kw={'class':'form-control',"placeholder":"Enter Phone"}
    )
    
    submit=SubmitField(
        "Register",
        render_kw={'class':'btn btn-primary btn-sm'}
    )
   
    def validate_email(self,email):
        if Account.query.filter_by(email=email.data).first():
            raise ValidationError("Email đã tồn tại vui lòng chọ email khác!") 
        



class LoginForm(FlaskForm):
   
    email=StringField(
        "Email",
          validators=[DataRequired(),Email()],
          render_kw={'class':'form-control',"placeholder":"Enter email"}
    )
    password=PasswordField(
        "Password",
          validators=[DataRequired(),Length(min=6,max=32,message="Password chỉ nhập từ 6-32 kí tự"),
                      Regexp('^[a-zA-Z0-9]*$',message="Password chỉ dược phép nhập kí tự và số")],
          render_kw={'class':'form-control',"placeholder":"Enter Password"}
    )
    remember=BooleanField(
        "Remember me!",default=True
    )
    
    submit=SubmitField(
        "Login",
        render_kw={'class':'btn btn-primary btn-sm'}
    )


class ForgetForm(FlaskForm):
   
    email=StringField(
        "Email",
          validators=[DataRequired(),Email()],
          render_kw={'class':'form-control',"placeholder":"Enter email"}
    )
    phone=StringField(
        "Phone",
          validators=[DataRequired(),Length(min=10,max=12,message="Phone chỉ nhập từ 10-12 kí tự"),
                      Regexp('^[0-9]*$',message="Phone chỉ dược phép nhập số")],
          render_kw={'class':'form-control',"placeholder":"Enter Phone"}
    )
    
    
    submit=SubmitField(
        "Khôi Phục",
        render_kw={'class':'btn btn-primary btn-sm'}
    )