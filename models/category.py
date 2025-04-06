from shop import db
from datetime import datetime


class Category(db.Model):
    __tablename__="categories"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    desc=db.Column(db.Text,nullable=False)
    create_at=db.Column(db.DateTime,default=datetime.utcnow)
    update_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.now)
    is_active=db.Column(db.Boolean,default=True)
    parent_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=True)
    parent=db.relationship("Category",remote_side=[id],backref='children')

    def __repr__(self):
        return f'<Category {self.name} >'
