from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)

    def __str__(self):
        return self.name


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name='Admin', username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        db.session.add(u)
        db.session.commit()

        c1 = Category(mname='Mobile')
        c2 = Category(name='Tablet')
        c3 = Category(name='Desktop')
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()

        p1 = Product(name='iPhone 13', price=22000000, category_id=1)
        p2 = Product(name='Galaxy Tab S9', price=28000000, category_id=2)
        p3 = Product(name='iPad Pro 2023', price=21000000, category_id=2)
        p4 = Product(name='Galaxy S23', price=18000000, category_id=1)
        p5 = Product(name='iPhone 15', price=22000000, category_id=1)
        db.session.add_all([p1, p2, p3, p4, p5])
        db.session.comit()