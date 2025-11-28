from functools import wraps
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, SQLAlchemyError
from sqlalchemy.orm.exc import UnmappedInstanceError
from ..config import session, get_session
from .logger import logger
import streamlit as st
import dotenv
import os
dotenv.load_dotenv()



global db_password
db_password = os.getenv("password")

def transaction(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
    
        if not hasattr(self, 'session'):
             self.session = get_session()
        
        session = self.session
        
        key = f"tx_{func.__name__}"

        if key not in st.session_state:
            st.session_state[key] = "ask"

        if st.session_state[key] == "ask":
            st.warning(f" Are you sure you want to execute **{func.__name__}**?")
            col1,col2 = st.columns(2)
            
            if col1.button("Commit", key=f"btn_commit_{key}"):
                st.session_state[key] = "commit"
                st.rerun()
            
            if col2.button("Rollback", key=f"btn_rollback_{key}"):
                st.session_state[key] = "rollback"
                st.rerun()
            
            st.stop()

        elif st.session_state[key] == "commit":
            try:
                result = func(self, *args, **kwargs)
                session.commit()
                st.success(f"Transaction committed for **{func.__name__}**")
                logger.info(f"Transaction committed for {func.__name__}")

                del st.session_state[key]
                return result
            except (ValueError, IntegrityError, DataError, OperationalError, ValueError, TypeError, AttributeError,SQLAlchemyError) as e:
                session.rollback()
                st.error(f" Error: {e}")
                logger.error(f"Error in {func.__name__}: {e}")
                del st.session_state[key]
                return None

        elif st.session_state[key] == "rollback":
            session.rollback()
            st.warning(f"Transaction rolled back for **{func.__name__}**")
            logger.info(f"Transaction rolled back for {func.__name__}")
            del st.session_state[key]
            return None
        
        return None

    return wrapper


def exception_handling(func):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        
        if not hasattr(self, 'session'):
             self.session = get_session()
        
        session = self.session
        try:
            result = func(self,*args, **kwargs)
            session.commit()
            return result
        
        except (ValueError, IntegrityError, DataError, OperationalError, ValueError, TypeError, AttributeError,SQLAlchemyError) as e:
            session.rollback()
            logger.warning(f" Warning in {func.__name__}: {e}", exc_info=False)
            st.error(f" Warning: {e}")
            raise
            

        except Exception as e:
            session.rollback()
            logger.error(f" Critical error in {func.__name__}: {type(e).__name__} - {e}", exc_info=True)
            st.error(f" Critical Error: {type(e).__name__} - {e}")
            raise
        finally:
            session.close()
    return wrapper




def optional_filters(model, field1, field2):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                
                if not hasattr(self, 'session'):
                    self.session = get_session()
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

            except (ValueError, IntegrityError, DataError, OperationalError, TypeError, AttributeError, SQLAlchemyError) as e:
                logger.warning(f"Error in {func.__name__}", exc_info=True)
                st.error(f" error: {e}")
                raise

        return wrapper
    return decorator


def login_role_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
        
            key = f"login_{func.__name__}"
            if key not in st.session_state:
                st.session_state[key] = "ask"

            if st.session_state[key] == "ask":
                st.info(f" Admin authorization required to execute **{func.__name__}**")
                with st.form(key=f"form_{key}"):
                    role = st.text_input("Role")
                    pwd = st.text_input("Password", type="password")
                    submitted = st.form_submit_button("Proceed")
                    
                    if submitted:
                        st.session_state[f"{key}_role"] = role
                        st.session_state[f"{key}_pwd"] = pwd
                        st.session_state[key] = "check"
                        st.rerun()
                st.stop()

            if st.session_state[key] == "check":
                required_role = st.session_state.get(f"{key}_role", "").strip().lower()
                password = st.session_state.get(f"{key}_pwd", "").strip()
                
                if required_role == "admin" and password == db_password:
                    logger.info(f"{required_role} entered the Database successfully to execute {func.__name__}.")
                    st.success(f"WELCOME, {required_role}! You have access to execute {func.__name__}.")
                    result = func(self, *args, **kwargs)
                    if result is not None:
                        del st.session_state[key]
                        
                        if f"{key}_role" in st.session_state: del st.session_state[f"{key}_role"]
                        if f"{key}_pwd" in st.session_state: del st.session_state[f"{key}_pwd"]
                    return result
                else:
                    logger.warning(f"Incorrect DataBase Password attempt for {required_role} role.")
                    st.error(f"Incorrect database password or role.")
                    if st.button("Try Again", key=f"retry_{key}"):
                        st.session_state[key] = "ask"
                        st.rerun()
                    st.stop()
            
            return None

        return wrapper