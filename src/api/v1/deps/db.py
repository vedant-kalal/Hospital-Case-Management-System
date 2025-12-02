from src.config import Session

def get_db():
    db = Session()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()    
