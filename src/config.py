from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric , Boolean, Date, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()   
    
Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

session = Session()