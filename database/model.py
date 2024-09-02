from sqlalchemy import Column,Integer,String,ForeignKey,Float
from sqlalchemy.orm import relationship
from.database import Base


class UserInDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    #orders = relationship("Order", back_populates="user")
    carts = relationship("Cart", back_populates="user")


class ProductInDB(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key =True, index = True)
    product_name = Column(String)
    qty = Column(Integer)
    price = Column(Float)

    # orders = relationship("Order", back_populates="product")
    # carts = relationship("Cart", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")


class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    
    user = relationship("UserInDB", back_populates="carts")
    products = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    cart = relationship("Cart", back_populates="products")
    product = relationship("ProductInDB", back_populates="cart_items")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)
    
    user = relationship("UserInDB")
    #product = relationship("ProductInDB", back_populates="orders")
    products = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="products")
    product = relationship("ProductInDB", back_populates="order_items")
