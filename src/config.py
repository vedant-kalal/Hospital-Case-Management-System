from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric , Boolean, Date, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
Base = declarative_base()
DATABASE_URL = "mysql+pymysql://root:vedank10@localhost:3306/Hospital_case_management_system_db"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()