from functools import wraps
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, SQLAlchemyError
from sqlalchemy.orm.exc import UnmappedInstanceError
from ..config import session
from .logger import logger


global db_password
db_password = "vedank10"


def transaction(func):
    @wraps(func)
    def wrapper(self,*args, **kwargs):
        session = self.session
        try:
            result = func(self, *args, **kwargs)
            session.flush()
            logger.info(f"Are you sure you want to commit the transaction for {func.__name__}?")
            answer = input("Type 'yes' to commit, 'no' to rollback: ")
            if answer.lower().strip() == 'yes':
                session.commit()
                logger.info(f"answer was 'yes',Transaction committed for {func.__name__}")
                return result
            else:
                session.rollback()
                logger.info(f"answer was 'no',Transaction rolled back for {func.__name__}")

        except (ValueError, IntegrityError, DataError, OperationalError, ValueError, TypeError, AttributeError, UnmappedInstanceError, SQLAlchemyError) as e:
            session.rollback()
            logger.warning(f" Warning in {func.__name__}: {e}", exc_info=False)
            raise

        except Exception as e:
            session.rollback()
            logger.error(f" Critical error in {func.__name__}: {type(e).__name__} - {e}", exc_info=True)
            raise
        finally:
            try:
                session.close()
            except Exception:
                logger.exception("Failed to close session")

    return wrapper



def exception_handling(func):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        self.session = session
        try:
            result = func(self,*args, **kwargs)
            session.commit()
            return result
        
        except (ValueError, IntegrityError, DataError, OperationalError, ValueError, TypeError, AttributeError,SQLAlchemyError) as e:
            session.rollback()
            logger.warning(f" Warning in {func.__name__}: {e}", exc_info=False)
            raise

        except Exception as e:
            session.rollback()
            logger.error(f" Critical error in {func.__name__}: {type(e).__name__} - {e}", exc_info=True)
            raise
        finally:
            session.close()
    return wrapper



def expected_integer(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if args:
            value = args[0]       
        elif kwargs:
            value = list(kwargs.values())[0]   
        else:
            raise TypeError("Expected one integer parameter")
        
        if not isinstance(value, int):
            logger.warning(f"Invalid input type for {func.__name__}: "f"Expected integer but got {type(value).__name__}")
            raise TypeError(f"Invalid input type: Expected integer but got {type(value).__name__}")
        return func(self, *args, **kwargs)

    return wrapper



def optional_filters(model, field1, field2):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                session = self.session
                query = session.query(model)

                value1 = kwargs.get(field1, None)
                value2 = kwargs.get(field2, None)

                col1 = model.__table__.columns[field1]
                col2 = model.__table__.columns[field2]

                if value1 is None and value2 is None:
                    results = query.all()

                elif value1 is not None and value2 is None:
                    results = query.filter(col1 == value1).all()

                elif value1 is None and value2 is not None:
                    results = query.filter(col2 == value2).all()

                else:
                    results = query.filter(col1 == value1, col2 == value2).all()

                return func(self, *args, results=results, **kwargs)

            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                raise

        return wrapper
    return decorator



def login_role_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            required_role = input("Enter your role to proceed (doctor,nurse,admin,pharmacists,lab technicians): ").strip().lower()
            if required_role == "admin":
                password = input("Enter database password to proceed: ").strip()
                if password == db_password:
                    logger.info(f"{required_role} entered the Database successfully to execute {func.__name__}.")
                    print(f"WELCOME, {required_role}! , You have access to execute {func.__name__}.")
                    return func(self, *args, **kwargs)
                else:
                    logger.warning(f"Incorrect DataBase Password attempt for {required_role} role.")
                    raise PermissionError(f"Incorrect database password for {required_role} role.")
            else:
                logger.warning(f"Unauthorized access attempt to {func.__name__} with role {required_role}")
                raise PermissionError(f"Access denied: {required_role} role does not have permission to execute {func.__name__}.")
        return wrapper