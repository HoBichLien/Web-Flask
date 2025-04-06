import os
from flask import Flask,render_template,redirect,url_for,flash,request,Blueprint
from shop import db
from shop.models.category import Category
from shop.models.product import Product
from shop.forms.form_product import ProductForm
from werkzeug.utils import secure_filename
import time

pro_route=Blueprint('pro',__name__)

upload_folder='shop/static/upload/'
allow_extension={'png','jpg','gif','jpeg'}

def allow_files(filename):
     return'.' in filename and filename.rsplit('.',1)[1].lower() in allow_extension

@pro_route.route("/")
def index():
    sanpham=Product.query.all()
    return render_template('backend/product/list.html',products=sanpham)

@pro_route.route("/add",methods=['GET','POST'])
def add():
    form=ProductForm()
    form.category_id.choices=[(0,'--- Chọn Danh mục ---')]+[(c.id,c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        tenhinh="logo.png"
        if 'image' in request.files and allow_files(request.files['image'].filename):
            hinh=request.files['image']
            hinhgoc=secure_filename(hinh.filename)
            chuoi=str(int(time.time()))
            tenhinh=f'{chuoi}_{hinhgoc}' 
            hinh.save(os.path.join(upload_folder,tenhinh))

        sp=Product(
            name = form.name.data,
            desc = form.desc.data,
            price = form.price.data,
            category_id = form.category_id.data,
            is_active = form.is_active.data,
            image=tenhinh
            
        )
        db.session.add(sp)
        db.session.commit()
        flash("Thêm sản phẩm thành công","success")
        return redirect(url_for('hethong.pro.index'))
    return render_template('backend/product/form.html',form=form)

@pro_route.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    pro=Product.query.get_or_404(id)
    form=ProductForm(obj=pro)
    form.category_id.choices=[(0,'===chọn===')] +[ (c.id,c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        # kiểm tra hình
        if 'image' in request.files and  allow_files(request.files['image'].filename):
             #xóa hình cũ
            hinhcu=pro.image
            duongdan=os.path.join(upload_folder,hinhcu)
            if os.path.isfile(duongdan):
                os.remove(duongdan)
             #cập nhật hình mới
            hinh=request.files['image']
            hinhgoc=secure_filename(hinh.filename)
            chuoi=str(int(time.time()))#chuỗi thời gian upload ảnh
            tenhinh=f'{chuoi}_{hinhgoc}'#1717122_teenhinh.png
            hinh.save(os.path.join(upload_folder,tenhinh))
           
        else:
            tenhinh=pro.image
        # #sửa sản phẩm
        
        pro.name = form.name.data
        pro.desc=form.desc.data
        pro.price=form.price.data
        pro.category_id=form.category_id.data
        pro.is_active=form.is_active.data
        pro.image=tenhinh
        db.session.commit()
        flash("Sửa sản phẩm thành công","sucssecc")
        return redirect(url_for('hethong.pro.index'))
    return render_template("backend/product/form.html",form=form)

@pro_route.route("/delete/<int:id>")
def delete(id):
    sp=Product.query.get_or_404(id)
    tenhinh=sp.image
    duongdan=os.path.join(upload_folder,tenhinh)
    if os.path.isfile(duongdan):
        os.remove(duongdan)
    db.session.delete(sp)
    db.session.commit()
    flash("Xóa sản phẩm thành công","success")
    return redirect(url_for('hethong.pro.index'))