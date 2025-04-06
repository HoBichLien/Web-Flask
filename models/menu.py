from shop import db
from datetime import datetime


class MenuItem(db.Model):
    __tablename__="menus"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    url=db.Column(db.Text,nullable=True)
    order=db.Column(db.Integer,nullable=False,default=0)
    is_active=db.Column(db.Boolean,default=True)
    parent_id=db.Column(db.Integer,db.ForeignKey('menus.id'),nullable=True)
    childrent=db.relationship("MenuItem",backref=db.backref('parent',remote_side=[id]),lazy='dynamic')
    create_at=db.Column(db.DateTime,default=datetime.utcnow)
    update_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.now)
    def __repr__(self):
        return f'<MenuItem {self.name} >'
