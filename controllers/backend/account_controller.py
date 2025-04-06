import os
from flask import Flask,render_template,redirect,url_for,flash,request,Blueprint
from shop import db
from shop.models.account import Account
from shop.forms.form_backaccount import AccForm
from werkzeug.utils import secure_filename
import time

acc_route=Blueprint('acc',__name__)

upload_folder='shop/static/upload/'
allow_extension={'png','jpg','gif','jpeg'}

def allow_files(filename):
     return'.' in filename and filename.rsplit('.',1)[1].lower() in allow_extension

@acc_route.route("/")
def index():
    acc=Account.query.all()
    return render_template('backend/account/list.html',acc=acc)

@acc_route.route("/add",methods=['GET','POST'])
def add():
    form=AccForm()
    if form.validate_on_submit():
        tenhinh="logo.png"
        if 'image' in request.files and allow_files(request.files['image'].filename):
            hinh=request.files['image']
            hinhgoc=secure_filename(hinh.filename)
            chuoi=str(int(time.time()))
            tenhinh=f'{chuoi}_{hinhgoc}' 
            hinh.save(os.path.join(upload_folder,tenhinh))
        acc=Account(
            fullname=form.fullname.data,
            email=form.email.data,
            password=form.password.data,
            phone=form.phone.data,
            address=form.address.data,
            image=tenhinh,
            is_active=form.is_active.data,
            role=form.role.data,
            create_at=form.create_at.data,
            update_at=form.update_at.data
        )
        db.session.add(acc)
        db.session.commit()
        flash("Thêm account thành công","success")
        return redirect(url_for('hethong.acc.index'))
    return render_template('backend/account/form.html',form=form)

@acc_route.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    acc=Account.query.get_or_404(id)
    form=AccForm(obj=acc)
    if form.validate_on_submit():
        if 'image' in request.files and allow_files(request.files['image'].filename):
            hinhcu=acc.image
            duongdan=os.path.join(upload_folder,hinhcu)
            if os.path.isfile(duongdan):
                os.remove(duongdan)
            hinh=request.files['image']
            hinhgoc=secure_filename(hinh.filename)
            chuoi=str(int(time.time()))
            tenhinh=f'{chuoi}_{hinhgoc}'
            hinh.save(os.path.join(upload_folder,tenhinh))
        else:
            tenhinh=acc.image
        acc.fullname=form.fullname.data
        acc.address=form.address.data
        acc.image=tenhinh
        acc.is_active=form.is_active.data
        acc.role=form.role.data
        
        acc.update_at=form.update_at.data
        db.session.commit()
        flash("Sửa account thành công","sucssecc")
        return redirect(url_for('hethong.acc.index'))
    return render_template('backend/account/form.html',form=form)

@acc_route.route("/delete/<int:id>")
def delete(id):
    acc=Account.query.get_or_404(id)
    tenhinh=acc.image
    duongdan=os.path.join(upload_folder,tenhinh)
    if os.path.isfile(duongdan):
        os.remove(duongdan)
    db.session.delete(acc)
    db.session.commit()
    flash("xóa account thành công","success")
    return redirect(url_for('hethong.acc.index'))