from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Float
from sqlalchemy.orm import relationship
from.database import Base


class UserInDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    orders = relationship("Order", back_populates="user")
    carts = relationship("Cart", back_populates="user")


class ProductInDB(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key =True, index = True)
    product_name = Column(String)
    qty = Column(Integer)
    price = Column(Integer)

    orders = relationship("Order", back_populates="product")
    carts = relationship("Cart", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    
    user = relationship("UserInDB", back_populates="orders")
    product = relationship("ProductInDB", back_populates="orders")

class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    
    user = relationship("UserInDB", back_populates="carts")
    product = relationship("ProductInDB", back_populates="carts")