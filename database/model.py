from sqlalchemy import Column,Integer,String,Boolean
from.database import Base


class UserInDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class ProductInDB(Base):
    __tablename__ = "products"

    #user_id = Column()
    product_id = Column(Integer, primary_key =True, index = True)
    product_name = Column(String)
    qty = Column(Integer)
    price = Column(Integer)