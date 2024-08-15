from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base


user_name = "postgres"
password = "1234"
ip_address = "localhost"
port = "5432"
db_name = "postgres"

db_string = f"postgresql://{user_name}:{password}@{ip_address}:{port}/{db_name}"
engine = create_engine(db_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
