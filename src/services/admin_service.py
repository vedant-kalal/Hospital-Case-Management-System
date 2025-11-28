from ..config import Base, engine, get_session
from ..utils.logger import logger
from ..utils.decorators import transaction, login_role_required
import streamlit as st

class AdminService:
    def __init__(self):
        self.session = get_session()

    @login_role_required
    @transaction
    def create_tables(self):
        try:
            Base.metadata.create_all(engine)
            logger.info("All tables created successfully.")
            st.success("All tables created successfully.")
        except Exception as e:
            raise ValueError(f"Tables already exist or error occurred: {e}")

    @login_role_required
    @transaction
    def drop_tables(self):
        try:
            Base.metadata.drop_all(engine)
            logger.info("All tables dropped successfully.")
            st.success("All tables dropped successfully.")
        except Exception as e:
            raise ValueError(f"Tables Does not Exist or Error Occured {e}")
