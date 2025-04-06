from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField,FloatField,FileField
from wtforms.validators import DataRequired,Length,NumberRange,ValidationError
from shop.models.category import Category
from flask_ckeditor import CKEditorField

class ProductForm(FlaskForm):
    name=StringField(
        "Tên sản phẩm",
          validators=[DataRequired(),Length(min=6,max=160)],
          render_kw={'class':'form-control'}
    )
    desc=CKEditorField(
        "Mô tả",
          validators=[DataRequired(),Length(min=6)],
          render_kw={'class':'form-control'}
    )
    price=FloatField(
        "Giá sản phẩm",
          validators=[DataRequired(),NumberRange(min=0)],
          render_kw={'class':'form-control'}
    )
    image=FileField(
        "Hình sản phẩm",
          render_kw={'class':'form-control'}
    )
    is_active=BooleanField("Kích hoạt",default=True)
    category_id=SelectField(
        "Danh mục ",
          coerce=int,default=0,
          render_kw={'class':'form-control'}
    )
    submit=SubmitField(
        "Lưu",
        render_kw={'class':'btn btn-primary btn-sm'}
    )

    def validate_category_id(self,field):
        if not Category.query.get(field.data):
            raise ValidationError("vui lòng chọn danh mục")
   