from pydantic import BaseModel


class UserCreate(BaseModel):
    id : int
    username : str
    password : str


class UserOut(BaseModel):
    user_name : str

    class Config:
        from_attributes = True

class Products_create(BaseModel):
    productname : str
    quantity : int
    description : str
    price : int

class Products_out(BaseModel):
    id : int
    productname : str
    qty : int
    price : int

    class Config:
        from_atttributes = True


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    user_id: int
    products: list[CartItemCreate]

class OrderOut(BaseModel):
    id: int
    user_id: int
    user_name: str
    price: float

    class Config:
        from_atttributes = True

# class OrderCreate(BaseModel):
#     product_id: int
#     quantity: int

# class OrderOut(BaseModel):
#     id: int
#     user_id: int
#     product_id: int
#     quantity: int

#     class Config:
#         from_atttributes = True

# # class OrderUpdate(BaseModel):
# #     user_id: int
# #     product_id: int
# #     quantity: int

# class CartCreate(BaseModel):
#     product_id: int
#     quantity: int

# class CartOut(BaseModel):
#     id: int
#     user_id: int
#     product_id: int
#     quantity: int

#     class Config:
#         from_atttributes = True
