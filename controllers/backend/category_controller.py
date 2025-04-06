from flask import render_template,Blueprint,redirect,request,url_for
from shop.models.category import Category
from shop.forms.form_category import CategoryForm
from shop import db

cate_route=Blueprint('cate',__name__,template_folder='../../templates/backend/category')
@cate_route.route("/")
def index():
    categories=Category.query.all()
    return render_template('list.html',categories=categories)

@cate_route.route("/add",methods=['GET','POST'])
def add():
    form=CategoryForm()
    form.parent_id.choices=[(0,"-- Chọn Danh mục ---")] + [(cat.id,cat.name) for cat in Category.query.all()]
    if form.validate_on_submit():
        new_cate=Category(
            name=form.name.data,
            desc=form.desc.data,
            is_active=form.is_active.data,
            parent_id=form.parent_id.data if form.parent_id.data !=0 else None
            
        )
        db.session.add(new_cate)
        db.session.commit()
        return redirect(url_for('hethong.cate.index'))
    return render_template('form.html',form=form)

@cate_route.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    cate=Category.query.get_or_404(id)
    form=CategoryForm(obj=cate)
    form.parent_id.choices=[(0,"-- Chọn Danh mục ---")] + [(cat.id,cat.name) for cat in Category.query.all() if cat.id!=id]
    if form.validate_on_submit():
        cate.name=form.name.data
        cate.desc=form.desc.data
        cate.is_active=form.is_active.data
        cate.parent_id=form.parent_id.data if form.parent_id.data !=0 else None
        db.session.commit()
        return redirect(url_for('hethong.cate.index'))
    return render_template('form.html',form=form)

@cate_route.route("/delete/<int:id>",methods=['GET','POST'])
def delete(id):
    cate=Category.query.get_or_404(id)
    db.session.delete(cate)
    db.session.commit()
    return redirect(url_for('hethong.cate.index'))