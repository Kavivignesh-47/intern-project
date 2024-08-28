from fastapi import FastAPI
from database.database import Base, engine
from routes import r_user,r_product

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(r_user.router_user)

app.include_router(r_product.router_product)