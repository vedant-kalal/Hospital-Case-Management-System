from ..models.health_center import HealthCenter
from ..config import session, get_session
from ..utils.logger import logger
from ..utils.decorators import transaction, exception_handling, optional_filters, login_role_required
from tabulate import tabulate
import streamlit as st
import pandas as pd


class HealthCenterService:
    def __init__(self):
        self.session = get_session()


    @transaction
    def add_health_center(self, name, address, is_active, created_at):

        new_health_center = HealthCenter(
            name=str(name),
            address=str(address),
            is_active=is_active,
            created_at=created_at,
        )
        self.session.add(new_health_center)
        logger.info(f"Added new health center: {name} , Address: {address}, is_active: {is_active}, created_at: {created_at}")
        st.info(f"Health Center: **{name}**  ,  Address: **{address}**  ,  is_active: **{is_active}**  ,  created_at: **{created_at}**  ,  Added successfully.")
        return new_health_center
    


    @exception_handling
    def fetch_health_center_by_id(self, health_center_id):
        health_center = self.session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        
        if health_center is not None:
            df = pd.DataFrame([{
                "ID": health_center.id,
                "Name": health_center.name,
                "Address": health_center.address,
                "Active": health_center.is_active,
                "Created At": health_center.created_at
            }])
            table = [[health_center.id, health_center.name, health_center.address, health_center.is_active, health_center.created_at] for health_center in [health_center]]
            st.success(f"Fetched Health Center ID {health_center_id} successfully.")
            st.table(df)
            logger.info(f"Fetched health center by ID {health_center_id} :- "
                        +"\n" + tabulate(
                            table,
                            headers=["ID", "Name", "Address", "Active", "Created At"],
                            tablefmt="grid"
                        ))
        else:
            st.error(f" Health center with ID {health_center_id} does not exist.")
            logger.error(f"Health center with ID {health_center_id} does not exist.")
        return health_center



    @optional_filters(HealthCenter, 'is_active', 'name')
    @exception_handling
    def fetch_health_centers_by_OptionalFilters(self, name=None, is_active=None, results=None):
        if results:
            df = pd.DataFrame([{
                "ID": hc.id,
                "Name": hc.name,
                "Address": hc.address,
                "Active": hc.is_active,
                "Created At": hc.created_at
            } for hc in results])
            
            table = [[hc.id, hc.name, hc.address, hc.is_active, hc.created_at] for hc in results]
            st.success(f"Fetched Health Centers with filters - Name: {name} , is_active: {is_active}")
            st.table(df)
            logger.info("\n" + tabulate(
                table,
                headers=["ID", "Name", "Address", "Active", "Created At"],
                tablefmt="grid"
            ) + "\n")
        else:
            st.error(f"No matching health centers found , with is_active={is_active} and name={name}")
            logger.warning(f"No matching health centers found , with is_active={is_active} and name={name}")

        return results
    

    @login_role_required
    @transaction
    def update_health_center(self, health_center_id, name=None, address=None, is_active=None):
        health_center = self.session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        if not health_center:
            st.error(f" Health center with ID {health_center_id} does not exist.")
            logger.error(f"Health center with ID {health_center_id} does not exist.")
            

        if name is not None:
            health_center.name = name
        if address is not None:
            health_center.address = address
        if is_active is not None:
            health_center.is_active = is_active

        df = pd.DataFrame([{
            "ID": hc.id,
            "Name": hc.name,
            "Address": hc.address,
            "Active": hc.is_active,
            "Created At": hc.created_at
        } for hc in [health_center]])

        st.success(f"Updated Health Center ID {health_center_id} successfully.")
        st.table(df)
        
        table = [[health_center.id, health_center.name, health_center.address, health_center.is_active, health_center.created_at]]
        logger.info(f"Updated health center ID {health_center_id} with values: "+ "\n" + tabulate(
            table,
            headers=["ID", "Name", "Address", "Active", "Created At"],
            tablefmt="grid"
        ))
        
        return health_center
    
        
    @login_role_required
    @transaction
    def delete_health_center(self, health_center_id):
        health_center = self.session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()

        if not health_center:
            st.error(f" Health center with ID {health_center_id} does not exist.")
            logger.warning(f"Health center with ID {health_center_id} does not exist.")
            
        else:
            self.session.delete(health_center)
            st.success(f"Deleted Health Center ID {health_center_id} successfully.")
            logger.info(f"Deleted health center with ID {health_center_id}.")
            return True
        return False