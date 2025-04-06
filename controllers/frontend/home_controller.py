from flask import render_template,Blueprint,request,url_for,redirect,Response,session,jsonify,flash
from shop.models.menu import MenuItem
from shop.models.product import Product,Order,OrderDetail
from shop.models.category import Category
from shop.models.contact import Contact
from datetime import datetime
from shop.utils import generate_slug
from html import escape  # Import để mã hóa ký tự đặc biệt trong XML
from shop.forms.form_profile import ProfileForm
from shop.forms.form_contact import ContactForm
from shop.models.account import Account
from flask_login import current_user,login_required
from flask_mail import Mail, Message
from shop import mail

from shop import db,bcrypt
import os
from werkzeug.utils import secure_filename
import time

h_route=Blueprint('home',__name__,template_folder='../../templates/frontend')

def menu_list(items):
    html=''
    for item in items:
        if item.is_active:
            if item.childrent.count()>0:
                #hiển thị dropdown
                html+=f'''
                       <div class="nav-item dropdown">
                            <a href="" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">{item.name}</a>
                            <div class="dropdown-menu m-0 bg-secondary rounded-0">
                                {menu_list(item.childrent)}
                                
                            </div>
                        </div>
                '''
            else:
                html+=f'<a href="{item.url}" class="nav-item nav-link">{item.name}</a>'
    return html

@h_route.route("/")
def index():
    try:
        title="ỐP ĐIỆN THOẠI CHO DẾ YÊU"
        keyword="Ốp điện thoại"
        description="Sản phẩm hot"
        menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()
        menu_home=menu_list(menu_item)
        list_all=(Product.query
                .filter_by(is_active=True)
                .order_by(Product.create_at.desc())
                .limit(8)
                .all()
                )
        list_1=(Product.query
                .filter_by(is_active=True,category_id=3)
                .order_by(Product.create_at.desc())
                .limit(8)
                .all()
                )
        list_2=(Product.query
                .filter_by(is_active=True,category_id=4)
                .order_by(Product.create_at.desc())
                .limit(8)
                .all()
                )
        list_3=(Product.query
                .filter_by(is_active=True,category_id=5)
                .order_by(Product.create_at.desc())
                .limit(8)
                .all()
                )
        list_4=(Product.query
                .filter_by(is_active=True,category_id=6)
                .order_by(Product.create_at.desc())
                .limit(8)
                .all()
                )
        list_11=(Product.query
                .filter_by(is_active=True,category_id=3)
                .order_by(Product.create_at.desc())
                .limit(6)
                .all()
                )
        list_12=(Product.query
                .filter_by(is_active=True,category_id=4)
                .order_by(Product.create_at.desc())
                .limit(4)
                .all()
                )
        return render_template('pages/home.html',**locals())
    except Exception as e:
        print(e)
        return redirect (url_for("home.notfound"))

@h_route.route("/category")
def category():
        
    try:
        title=" DANH MỤC ỐP ĐIỆN THOẠI CHO DẾ YÊU"
        keyword="Ốp điện thoại"
        description="Sản phẩm hot"
        menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).order_by(MenuItem.order).all()
        menu_home=menu_list(menu_item)

        #lấy tất cả sản phẩm có is_active=True
        query=Product.query.filter_by(is_active=True)
        
        #phân trang
        page=request.args.get('page',1,type=int)
        per_page=9       
        
        # tìm kiếm theo từ khóa
        tim=request.args.get('search')
        if tim:
            query=query.filter(Product.name.ilike(f'%{tim}%'))

        #tìm kiếm theo danh mục
        cate=Category.query.all()
        id_dm=request.args.get('cat_id',type=int)
        if id_dm:
            query=query.filter_by(category_id=id_dm)

        #lấy sản phẩm nổi bật
        feature=Product.query.filter_by(is_active=True).order_by(Product.create_at.desc()).limit(3).all()
        
        #tìm kiếm theo sort
        sapxep=request.args.get('sort',type=int)
        if sapxep=='price_asc':
            query=query.order_by(Product.price.asc())
        elif sapxep=='price_desc':
             query=query.order_by(Product.price.desc())
        elif sapxep=='date_desc':
             query=query.order_by(Product.create_at.desc()) 
        elif sapxep=='price_asc':
             query=query.order_by(Product.create_at.asc())    

        #tìm kiếm theo kéo thanh sort
        min_p=request.args.get("min_price",type=float,default=0)
        max_p=request.args.get("max_price",type=float)
        #lọc theo khoảng giá
        if min_p:
            query=query.filter(Product.price >= min_p )
        if max_p:
            query=query.filter(Product.price <= max_p )

         
        product_list=query.paginate(page=page,per_page=per_page)  
        sanpham=product_list.items
        pages = product_list.pages 
        return render_template('pages/category.html',**locals())
    except Exception as e:
        print(e)
        return redirect (url_for("home.notfound"))

@h_route.route("/not-found")
def notfound():
    menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()
    return render_template('pages/notfound.html',menu_home=menu_list(menu_item))
@h_route.route("/product")
def product():
    menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()
    return render_template('pages/product.html',menu_home=menu_list(menu_item))

@h_route.route("/<name>-<int:id>")
def detail(name,id):
    try:
        menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()
        menu_home=menu_list(menu_item)
        sp=Product.query.get_or_404(id)
        cate=Category.query.all()
        title=sp.name
        keyword=sp.name
        description=sp.desc
        hot=Product.query.filter(Product.is_active==True).limit(4).all()
        splq=Product.query.filter(
            Product.category_id==sp.category_id,
            Product.id!=sp.id,
            Product.is_active==True
            ).limit(8).all()

        return render_template('pages/product.html',**locals())
    except Exception as e:
        print(e)
        return redirect (url_for("home.notfound"))

@h_route.route("/contact",methods=['GET','POST'])
def contact():
    title=" LIÊN HỆ ỐP ĐIỆN THOẠI CHO DẾ YÊU"
    keyword="Ốp điện thoại"
    description="Sản phẩm hot"
    menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()
    menu_home=menu_list(menu_item)

    form = ContactForm()
    if form.validate_on_submit():
        # Lưu vào database
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data
        )
        db.session.add(new_contact)
        db.session.commit()

        # Gửi email
        msg = Message('New Contact Message', recipients=['receiver_email@gmail.com'])
        msg.body = f"""
        Name: {form.name.data}
        Phone: {form.phone.data}
        Email: {form.email.data}
        Message: {form.message.data}
        """
        mail.send(msg)

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('home.contact'))
   
    return render_template('pages/contact.html',**locals())

@h_route.route('/cart', methods=['POST'])
def cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)
    
    if 'cart' not in session:
        session['cart'] = {}  #tạo giỏ hàng rỗng

    giohang = session['cart']
    #giỏ hàng siêu thị
    if str(product_id) in giohang:
        giohang[str(product_id)]['quantity'] += quantity
    else:
        sp = Product.query.get(product_id)
        if sp:
            giohang[str(product_id)] = {
                'name': sp.name,
                'price': sp.price,
                'quantity': quantity,
                'image': sp.image
            }
        else:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404

    session['cart'] = giohang
    session.modified = True  # lưu thay đổi trong session

    return jsonify({'status': 'success', 'cart': giohang})


@h_route.route('/shopping-cart')
def listcart():
    # try:
        title="GIỎ HÀNG ỐP ĐIỆN THOẠI CHO DẾ YÊU"
        keyword="Ốp điện thoại"
        description="Sản phẩm hot"
        menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).order_by(MenuItem.order).all()
        return render_template("pages/cart.html",menu_home=menu_list(menu_item))
    # except Exception as e:
    #     return redirect(url_for("home.index"))


@h_route.route('/shopping-delete',methods=['POST'])
def remove_cart():
    id=request.json.get('product_id')
    cart=session.get('cart',{})

    if str(id) in cart:
        del cart[str(id)]

    session['cart']=cart
    session.modified=True
    return jsonify({'status':'success','cart':cart})

@h_route.route('/update-cart',methods=['POST'])
def update_cart():
    product_id=request.json.get('id')
    soluong=request.json.get('sl',0)
    nhaptay=request.json.get('nhaptay',1)

    cart=session.get('cart',{})

    if str(product_id) not in cart:
        return jsonify({'success':False,"message":"Product not found"}),404
    
    sanpham=cart[str(product_id)]
    if nhaptay:
        new_quantity=max(1,soluong)
    else:
        new_quantity=max(1,sanpham['quantity']+soluong)

    
    #cap nhat lại so luong gio hang
    sanpham['quantity']=new_quantity

    #tổng giá mới
    productTotal=sanpham['price']*sanpham['quantity']
    cart_Total= sum(item['price']*item['quantity'] for item in cart.values())
    tongcoship=cart_Total+20000

    session['cart']=cart
    session.modified=True

    return jsonify({
        'success':True,
        'new_quantity':new_quantity,
        'productTotal':productTotal,
        'cart_Total':cart_Total,
        'tongcoship':tongcoship
    })

upload_folder='shop/static/upload/'
@h_route.route('/checkout',methods=['GET','POST'])
@login_required
def checkout():
    title="THANH TOÁN ỐP ĐIỆN THOẠI CHO DẾ YÊU"
    keyword="Ốp điện thoại"
    description="Sản phẩm hot"
    menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()
    menu_home=menu_list(menu_item)

    
    #tính tổng tiền
    cart=session.get('cart',{})
    total_payment= sum(item['price']*item['quantity'] for item in cart.values())
    user=Account.query.filter_by(id=current_user.id).first()
    form=ProfileForm(obj=user)
    if form.validate_on_submit():   
        # Cập nhật thông tin từ form
        user.fullname=form.fullname.data
        user.phone=form.phone.data
        user.address=form.address.data
        if form.password.data:
            user.password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Lưu ảnh (nếu có)
        if 'image' in request.files:
            hinhcu=user.image
            duongdan=os.path.join(upload_folder,hinhcu)
            if os.path.isfile(duongdan):
                os.remove(duongdan)
            #cập hình mới
            hinh=request.files['image'] # kích thước, tên file hinh, đuôi hinh .png...
            hinhgoc=secure_filename(hinh.filename)
            chuoi=str(int(time.time())) #thơi gian upload ảnh
            tenhinh=f'{chuoi}_{hinhgoc}' #172767233_tenhinh.png
            hinh.save(os.path.join(upload_folder,tenhinh))        
        else:
            tenhinh=user.image
        
        user.image=tenhinh 
        db.session.commit()
        # lưu thông tin vào bảng order
        new_order=Order(
            user_id=user.id,
            total_payment=total_payment,

        )
        db.session.add(new_order)
        db.session.commit()
        #lưu chi tiết đơn hàng vào bảng order detail
        for key, item in cart.items():
            chitietdh=OrderDetail(
                order_id=new_order.id,
                product_name=item['name'],
                quantity=item['quantity'],
                price=item['price'],
                total=item['price']*item['quantity']
            )
            db.session.add(chitietdh)
            #cập nhật csdl
        db.session.commit()
        session.pop('cart',None)
        flash('Order place success!')

        return redirect(url_for('home.checkout'))  
    
    return render_template("pages/checkout.html",**locals())


@h_route.route("/sitemap.xml")
def sitemap():
    sanpham = Product.query.filter_by(is_active=True).all()  # Lấy tất cả sản phẩm
    danhmuc = Category.query.filter_by(is_active=True).all()  # Lấy tất cả danh mục

    baseurl = "http://127.0.0.1:5000/"
    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    # xml.append('<?xml-stylesheet type="text/xsl" href="/static/sitemap.xsl"?>')
    
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Tạo URL XML cho trang chủ
    xml.append(f""" 
       <url>
           <loc>{baseurl}</loc>
           <lastmod>{datetime.utcnow().date()}</lastmod>
           <changefreq>daily</changefreq>
           <priority>1.0</priority>
       </url>
    """)

    # Tạo URL XML cho danh mục
    for cate in danhmuc:
        cate_url = escape(url_for("home.category", cat_id=cate.id, _external=True))  # Escape URL
        xml.append(f""" 
            <url>
                <loc>{cate_url}</loc>
                <lastmod>{cate.update_at.date() if cate.update_at else datetime.utcnow().date()}</lastmod>
                <changefreq>daily</changefreq>
                <priority>0.9</priority>
            </url>
        """)

    # Tạo URL XML cho sản phẩm
    for sa in sanpham:
        sp_url = escape(url_for("home.detail", name=generate_slug(sa.name), id=sa.id, _external=True))  # Escape URL
        xml.append(f""" 
            <url>
                <loc>{sp_url}</loc>
                <lastmod>{sa.update_at.date() if sa.update_at else datetime.utcnow().date()}</lastmod>
                <changefreq>daily</changefreq>
                <priority>0.8</priority>
            </url>
        """)

    xml.append('</urlset>')
    res = Response("\n".join(xml), mimetype='application/xml')
    res.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return res


