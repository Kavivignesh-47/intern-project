from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from database.model import UserInDB, ProductInDB, Order, Cart, CartItem,OrderItem
from schemas.schemas import  OrderCreate, CartItemCreate, OrderCreate, OrderOut
from routes.r_product import get_db

router_cart = APIRouter()


@router_cart.post("/carts/{user_id}/add", status_code = status.HTTP_201_CREATED, tags=["Cart"])
def add_to_cart(user_id: int, cart_item: CartItemCreate, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not db_cart:
        db_cart = Cart(user_id=user_id)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)

    db_cart_item = CartItem(cart_id=db_cart.id, product_id=cart_item.product_id, quantity=cart_item.quantity)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

@router_cart.get("/cart/{cart_id}", tags=["Cart"])
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart

@router_cart.post("/orders/", status_code = status.HTTP_201_CREATED, tags=["Order"])
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(user_id=order.user_id, total_price=0)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    total_price = 0
    for item in order.products:
        db_item = db.query(ProductInDB).filter(ProductInDB.product_id == item.product_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Item with ID {item.product_id} not found")

        db_order_item = OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
        total_price += db_item.price * item.quantity
        db.add(db_order_item)

    db_order.total_price = total_price
    db.commit()
    db.refresh(db_order)

    return db_order

@router_cart.get("/orders/{order_id}",response_model = OrderOut, tags=["Order"])
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order :
        raise HTTPException(status_code=404, detail="Order not found")
    user_name = db.query(UserInDB).filter(UserInDB.id == db_order.user_id).first()
    return OrderOut(id = db_order.id, user_id = db_order.user_id, user_name = user_name.username, price = db_order.total_price)

# def create_cart(db: Session, user_id: int, cart: CartCreate):
#     db_cart = Cart(user_id=user_id, product_id=cart.product_id, quantity=cart.quantity)
#     db.add(db_cart)
#     db.commit()
#     db.refresh(db_cart)
#     return db_cart

# def get_cart(db: Session, user_id: int):
#     return db.query(Cart).filter(Cart.user_id == user_id).all()

# def get_cart_item(db: Session, user_id: int, product_id: int):
#     return db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()

# def update_cart(db: Session, user_id: int, cart: CartCreate):
#     db_cart = get_cart_item(db, user_id, cart.product_id)
#     if db_cart:
#         db_cart.quantity = cart.quantity
#     else:
#         db_cart = Cart(user_id=user_id, product_id=cart.product_id, quantity=cart.quantity)
#         db.add(db_cart)
#     db.commit()
#     db.refresh(db_cart)
#     return db_cart

# def delete_cart_item(db: Session, user_id: int, product_id: int):
#     db_cart = get_cart_item(db, user_id, product_id)
#     if db_cart:
#         db.delete(db_cart)
#         db.commit()
#         return True
#     return False

# @router_cart.post("/carts/", response_model=CartOut, tags=["Cart"], status_code=status.HTTP_201_CREATED)
# def add_to_cart(user_id: int, cart: CartCreate, db: Session = Depends(get_db)):
#     return create_cart(db=db, user_id=user_id, cart=cart)

# @router_cart.get("/carts/{user_id}", response_model=List[CartOut],tags=["Cart"], status_code=status.HTTP_200_OK)
# def get_user_cart(user_id: int, db: Session = Depends(get_db)):
#     return get_cart(db=db, user_id=user_id)

# @router_cart.put("/carts/{user_id}", response_model=CartOut, tags=["Cart"], status_code=status.HTTP_202_ACCEPTED)
# def update_cart_item(user_id: int, cart: CartCreate, db: Session = Depends(get_db)):
#     return update_cart(db=db, user_id=user_id, cart=cart)

# @router_cart.delete("/carts/{user_id}/{product_id}", response_model=bool, tags=["Cart"])
# def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
#     result = delete_cart_item(db=db, user_id=user_id, product_id=product_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Cart item not found")
#     return {"detail": "Cart item deleted successfully"}
