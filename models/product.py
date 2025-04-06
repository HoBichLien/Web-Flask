from shop import db
from datetime import datetime

class Product(db.Model):
    __tablename__="products"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    desc=db.Column(db.Text,nullable=False)
    create_at=db.Column(db.DateTime,default=datetime.utcnow)
    update_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.now)
    is_active=db.Column(db.Boolean,default=True)
    price=db.Column(db.Float,nullable=False)
    image=db.Column(db.String(150),nullable=False)
    category_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=True)
    category=db.relationship("Category",backref='products')
    

    def __repr__(self):
        return f'<Product {self.name} >'
    

    #order detail
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    total_payment = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)

class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)