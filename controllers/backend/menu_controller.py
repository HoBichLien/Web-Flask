from flask import render_template,Blueprint,redirect,request,url_for,flash
from shop.models.menu import MenuItem
from shop.forms.form_menu import MenuForm
from shop import db
from datetime import datetime

menu_route=Blueprint('menu',__name__)
@menu_route.route("/")
def index():
    menu=MenuItem.query.all()
    return render_template('backend/menu/list.html',menu=menu)

@menu_route.route("/add",methods=['GET','POST'])
def add():
    form=MenuForm()
    form.parent_id.choices=[(0,"-- Chọn Menu ---")] + [(mn.id,mn.name) for mn in MenuItem.query.all()]
    if form.validate_on_submit():
        new_menu=MenuItem(
            name=form.name.data,
            url=form.url.data,
            order=form.order.data,
            is_active=form.is_active.data,
            parent_id=form.parent_id.data if form.parent_id.data !=0 else None
            
        )
        db.session.add(new_menu)
        db.session.commit()
        flash("Thêm menu thành công","success")
        return redirect(url_for('hethong.menu.index'))
    return render_template('backend/menu/form.html',form=form)

@menu_route.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    menu=MenuItem.query.get_or_404(id)
    form=MenuForm(obj=menu)
    form.parent_id.choices=[(0,"-- Chọn Menu ---")] + [(mn.id,mn.name) for mn in MenuItem.query.all() if mn.id!=id]
    if form.validate_on_submit():
        menu.name=form.name.data
        menu.url=form.url.data
        menu.order=form.order.data
        menu.is_active=form.is_active.data
        menu.parent_id=form.parent_id.data if form.parent_id.data !=0 else None
        menu.update_at=datetime.utcnow()
        db.session.commit()
        flash("Sửa menu thành công","success")
        return redirect(url_for('hethong.menu.index'))
    return render_template('backend/menu/form.html',form=form)

@menu_route.route("/delete/<int:id>",methods=['GET','POST'])
def delete(id):
    menu=MenuItem.query.get_or_404(id)
    db.session.delete(menu)
    db.session.commit()
    flash("Xóa menu thành công","success")
    return redirect(url_for('hethong.menu.index'))