from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.model import ProductInDB
from database.database import SessionLocal
from schemas.schemas import Products_create, Products_out

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


