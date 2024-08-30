from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.model import ProductInDB, Order
from database.database import SessionLocal
from schemas.schemas import Products_create, Products_out, OrderCreate, OrderOut, OrderUpdate
from authentication.authentication import get_product, create_order

router_product = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_product.post("/add_product", response_model=Products_out, tags=["Products"], status_code=status.HTTP_201_CREATED)
def create(request: Products_create, db: Session = Depends(get_db)):
    existing_product = db.query(ProductInDB).filter(ProductInDB.product_name == request.productname).first()
    if existing_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this name already exists")

    new_product = ProductInDB(
        product_name=request.productname,
        qty=request.quantity,
        price=request.price
    )
    #try:
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    # except IntegrityError:
    #     db.rollback()
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this name already exists")
    
    return Products_out(
        id=new_product.product_id,
        productname=new_product.product_name,
        qty=new_product.qty,
        price=new_product.price
    )

@router_product.get("/show_product/{prod_id}", response_model=Products_out, tags=["Products"])
def show(prod_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductInDB).filter(ProductInDB.product_id == prod_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {prod_id} not found")
    return Products_out(
        id=product.product_id,
        productname=product.product_name,
        qty=product.qty,
        price=product.price
    )

@router_product.delete("/delete_product/{prod_id}", tags=["Products"], status_code=status.HTTP_204_NO_CONTENT)
def delete(prod_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductInDB).filter(ProductInDB.product_id == prod_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {prod_id} not found")

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

@router_product.put("/update_product/{prod_id}", tags=["Products"], status_code=status.HTTP_202_ACCEPTED)
def update(prod_id: int, request: Products_create, db: Session = Depends(get_db)):
    product = db.query(ProductInDB).filter(ProductInDB.product_id == prod_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {prod_id} not found")

    product.product_name = request.productname
    product.qty = request.quantity
    product.price = request.price

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this name already exists")
    
    return {"detail": "Product updated successfully"}

@router_product.post("/orders/", response_model=OrderOut, tags=["Orders"], status_code = status.HTTP_201_CREATED)
def add_order(user_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    product = get_product(db, order.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return create_order(db=db, user_id=user_id, order=order)

@router_product.get("/orders/{order_id}", response_model=OrderOut, tags=["Orders"], status_code = status.HTTP_200_OK)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity
    )

@router_product.put("/update_order/{order_id}", tags=["Orders"], status_code=status.HTTP_202_ACCEPTED)
def update(order_id: int, request: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")

    order.user_id = request.user_id
    order.product_id = request.product_id
    order.quantity = request.quantity

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order with this id already exists")
    
    return {"detail": "Order updated successfully"}

@router_product.delete("/delete_order/{order_id}", tags=["Orders"], status_code=status.HTTP_204_NO_CONTENT)
def delete(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {order_id} not found")

    db.delete(order)
    db.commit()
    return {"detail": "Order id {order_id} deleted successfully"}