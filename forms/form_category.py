from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_ckeditor import CKEditorField

class CategoryForm(FlaskForm):
    name=StringField(
        "Tên danh mục",
          validators=[DataRequired(),Length(min=6,max=160)],
          render_kw={'class':'form-control'}
    )
    desc=CKEditorField(
        "Mô tả",
          validators=[DataRequired(),Length(min=6,max=160)],
          render_kw={'class':'form-control'}
    )
    is_active=BooleanField("Kích hoạt",default=True)
    parent_id=SelectField(
        "Danh mục cha",
          coerce=int,default=0,
          render_kw={'class':'form-control'}
    )
    submit=SubmitField(
        "Lưu",
        render_kw={'class':'btn btn-primary btn-sm'}
    )
   