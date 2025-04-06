from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SelectField,SubmitField,PasswordField,FileField,DateField
from wtforms.validators import DataRequired,Length,Email,Regexp,ValidationError
from shop.models.account import Account



class AccForm(FlaskForm):
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
    address=StringField(
        "Address ",
          validators=[DataRequired()],
          render_kw={'class':'form-control',"placeholder":"Enter address"}
    )
    image=FileField(
        "Hình user",
          render_kw={'class':'form-control'}
    )
    is_active=BooleanField("Kích hoạt",default=True)
    role=StringField(
        "role ",
          validators=[DataRequired()],
          render_kw={'class':'form-control',"placeholder":"Enter role"}
    )
    create_at=DateField(
        "Date create ",
          validators=[DataRequired()],
          render_kw={'class':'form-control',"placeholder":"Enter date create"}
    )
    update_at=DateField(
        "Date edit ",
          validators=[DataRequired()],
          render_kw={'class':'form-control',"placeholder":"Enter date edit"}
    )
    submit=SubmitField(
        "save",
        render_kw={'class':'btn btn-primary btn-sm'}
    )
   
    def validate_email(self, email):
    # Lấy account_id nếu có, trong trường hợp chỉnh sửa tài khoản
      id = getattr(self, 'account_id', None)

      # Nếu là tài khoản mới, kiểm tra email trùng
      if not id:
          if Account.query.filter_by(email=email.data).first():
              raise ValidationError("Email đã tồn tại, vui lòng chọn email khác!")

      # Nếu là chỉnh sửa tài khoản
      else:
          account = Account.query.get(id)
          if account:
              # Nếu email mới khác email cũ, kiểm tra email mới có trùng không
              if account.email != email.data:  # Chỉ kiểm tra nếu email mới khác email cũ
                  if Account.query.filter_by(email=email.data).first():
                      raise ValidationError("Email đã tồn tại, vui lòng chọn email khác!")
                  else:
                      pass


       