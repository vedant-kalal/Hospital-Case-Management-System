from ..models.clinician import Clinician
from ..models.health_center import HealthCenter
from ..config import session, get_session
from ..utils.logger import logger
from ..utils.decorators import transaction, exception_handling,  optional_filters, login_role_required
from tabulate import tabulate
import streamlit as st
import pandas as pd


class ClinicianService:
    def __init__(self):
        self.session = get_session()



    @transaction
    def add_clinician(self,name,health_center_id,email,role,is_active):
        
        
        health_center = self.session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        if not health_center:
            raise ValueError(f"Health Center with ID {health_center_id} does not exist.")

        
        existing_clinician = self.session.query(Clinician).filter(Clinician.email == email).first()
        if existing_clinician:
            raise ValueError(f"Clinician with Email {email} already exists.")

        new_clinician = Clinician(
            name=str(name),
            health_center_id=health_center_id,
            email=str(email),
            role=str(role),
            is_active=is_active,
        )
        session.add(new_clinician)
        
        
        logger.info(f"Added new clinician: {name} , Health Center ID: {health_center_id}, Email: {email}, Role: {role}, is_active: {is_active}")
        st.info(f"Added new clinician: **{name}** , Health Center ID: **{health_center_id}**, Email: **{email}**, Role: **{role}**, is_active: **{is_active}**")
        return new_clinician
    


    @exception_handling
    def fetch_by_clinician_id(self, clinician_id):
        clinician = self.session.query(Clinician).filter(Clinician.id == clinician_id).first()

        if clinician is not None:
            df = pd.DataFrame([{
                "ID": clinician.id,
                "Health Center ID": clinician.health_center_id,
                "Name": clinician.name,
                "Email": clinician.email,
                "Role": clinician.role,
                "Active": clinician.is_active
            }])
            table = [[clinician.id,clinician.health_center_id, clinician.name, clinician.email, clinician.role, clinician.is_active] for clinician in [clinician]]
            st.success(f"Fetched Clinician ID {clinician_id} successfully.")
            st.table(df)
            logger.info(f"Fetched clinician by ID {clinician_id} :- "
                        +"\n" + tabulate(
                            table,
                            headers=["ID", "Health Center ID", "Name", "Email", "Role", "Active"],
                            tablefmt="grid"
                        ))
        else:
            st.error(f" Clinician with ID {clinician_id} does not exist.")
            logger.error(f"Clinician with ID {clinician_id} does not exist.")

        return clinician



    @optional_filters(Clinician, 'is_active', 'name')
    @exception_handling
    def fetch_clinicians_by_OptionalFilters(self, name=None, is_active=None, results=None):
        table = [[hc.id, hc.health_center_id, hc.name, hc.email, hc.role, hc.is_active] for hc in results]
        if results:
            df = pd.DataFrame([{
                "ID": hc.id,
                "Health Center ID": hc.health_center_id,
                "Name": hc.name,
                "Email": hc.email,
                "Role": hc.role,
                "Active": hc.is_active
            } for hc in results])
            table = [[hc.id, hc.health_center_id, hc.name, hc.email, hc.role, hc.is_active] for hc in results]
            st.success(f"Fetched Clinicians with filters - Name: {name} , is_active: {is_active}")
            st.table(df)
            logger.info("\n" + tabulate(
                table,
                headers=["ID", "Health Center ID", "Name", "Email", "Role", "Active"],
                tablefmt="grid"
            ) + "\n")
        else:
            st.error(f"No matching clinicians found , with is_active={is_active} and name={name}")
            logger.error(f"No matching clinicians found , with is_active={is_active} and name={name}")
        return results
    
    
    

    @login_role_required
    @transaction
    def update_clinician(self, clinician_id, name=None, health_center_id=None, email=None, role=None ,is_active=None):
        clinician = self.session.query(Clinician).filter(Clinician.id == clinician_id).first()
        health_center = self.session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        if not health_center:
            raise ValueError(f"Health Center with ID {health_center_id} does not exist.")

        
        existing_clinician = self.session.query(Clinician).filter(Clinician.email == email).first()
        if existing_clinician:
            raise ValueError(f"Clinician with Email {email} already exists.")

        if not clinician:
            st.error(f" Clinician with ID {clinician_id} does not exist.")
            logger.error(f"Clinician with ID {clinician_id} does not exist.")

        if name is not None:
            clinician.name = name
        if health_center_id is not None:
            clinician.health_center_id = health_center_id
        if email is not None:
            clinician.email = email
        if role is not None:
            clinician.role = role
        if is_active is not None:
            clinician.is_active = is_active

        df = pd.DataFrame([{
                "ID": clinician.id,
                "Health Center ID": clinician.health_center_id,
                "Name": clinician.name,
                "Email": clinician.email,
                "Role": clinician.role,
                "Active": clinician.is_active
            } for clinician in [clinician]])
        
        st.success(f"Updated Clinician ID {clinician_id} successfully.")
        st.table(df)

        table = [[clinician.id, clinician.health_center_id, clinician.name, clinician.email, clinician.role, clinician.is_active]]
        logger.info(f"Updated clinician ID {clinician_id} with values: "+ "\n" + tabulate(
            table,
            headers=["ID", "Health Center ID", "Name", "Email", "Role", "Active"],
            tablefmt="grid"
        ))
        return clinician

    
  
    @login_role_required
    @transaction
    def delete_clinician(self, clinician_id):
        clinician = self.session.query(Clinician).filter(Clinician.id == clinician_id).first()

        if not clinician:
            logger.warning(f"Clinician with ID {clinician_id} does not exist.")
            
            raise ValueError(f"Clinician with ID {clinician_id} does not exist.")
            
        else:
            self.session.delete(clinician)
            st.success(f"Deleted Clinician ID {clinician_id} successfully.")
            logger.info(f"Deleted clinician with ID {clinician_id}.")
            return True
        return False
        
    

