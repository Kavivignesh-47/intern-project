from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from database.model import UserInDB, ProductInDB, Order, Cart
from schemas.schemas import UserCreate, Products_create, OrderCreate, CartCreate, CartOut
from routes.r_product import get_db

router_cart = APIRouter()

def create_cart(db: Session, user_id: int, cart: CartCreate):
    db_cart = Cart(user_id=user_id, product_id=cart.product_id, quantity=cart.quantity)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).all()

def get_cart_item(db: Session, user_id: int, product_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()

def update_cart(db: Session, user_id: int, cart: CartCreate):
    db_cart = get_cart_item(db, user_id, cart.product_id)
    if db_cart:
        db_cart.quantity = cart.quantity
    else:
        db_cart = Cart(user_id=user_id, product_id=cart.product_id, quantity=cart.quantity)
        db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def delete_cart_item(db: Session, user_id: int, product_id: int):
    db_cart = get_cart_item(db, user_id, product_id)
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return True
    return False

@router_cart.post("/carts/", response_model=CartOut, tags=["Cart"], status_code=status.HTTP_201_CREATED)
def add_to_cart(user_id: int, cart: CartCreate, db: Session = Depends(get_db)):
    return create_cart(db=db, user_id=user_id, cart=cart)

@router_cart.get("/carts/{user_id}", response_model=List[CartOut],tags=["Cart"], status_code=status.HTTP_200_OK)
def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    return get_cart(db=db, user_id=user_id)

@router_cart.put("/carts/{user_id}", response_model=CartOut, tags=["Cart"], status_code=status.HTTP_202_ACCEPTED)
def update_cart_item(user_id: int, cart: CartCreate, db: Session = Depends(get_db)):
    return update_cart(db=db, user_id=user_id, cart=cart)

@router_cart.delete("/carts/{user_id}/{product_id}", response_model=bool, tags=["Cart"])
def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    result = delete_cart_item(db=db, user_id=user_id, product_id=product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"detail": "Cart item deleted successfully"}
