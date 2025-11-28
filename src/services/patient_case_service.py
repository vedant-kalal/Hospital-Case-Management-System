from ..models.patient_case import PatientCase
from ..models.clinician import Clinician
from ..models.health_center import HealthCenter
from ..config import session,get_session
from ..utils.logger import logger
from ..utils.decorators import transaction, exception_handling, optional_filters, login_role_required
from tabulate import tabulate
import streamlit as st
import pandas as pd


class PatientCaseService:
    def __init__(self):
        self.session = get_session()


    @transaction
    def add_patient_case(self, health_center_id, clinician_id, patient_name, patient_dob, summary, status, created_at, updated_at):
        
        health_center = self.session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        clinician = self.session.query(Clinician).filter(Clinician.id == clinician_id).first()
        if not health_center:
            raise ValueError(f"Health Center with ID {health_center_id} does not exist.")
            
            
        if not clinician:
            
            logger.warning(f"Clinician with ID {clinician_id} does not exist.")
            raise ValueError(f"Clinician with ID {clinician_id} does not exist.")   
        
        new_patient_case = PatientCase(
            health_center_id=health_center_id,
            clinician_id=clinician_id,
            patient_name=patient_name,
            patient_dob=patient_dob,
            summary=summary,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )
        if status.lower() not in ['open', 'closed']:
            raise ValueError("Wrong Status must be either 'open' or 'closed'.")
        status = status.lower()
        self.session.add(new_patient_case)
        logger.info(f"Added new patient case: {patient_name} , Health Center ID: {health_center_id}, Clinician ID: {clinician_id}, Patient DOB: {patient_dob}, Status: {status}"+"\n"+
                    f", Summary: {summary}"+"\n"+
                    f"Created At: {created_at}, Updated At: {updated_at}")
        st.info(f"Added new patient case: {patient_name} , Health Center ID: {health_center_id}, Clinician ID: {clinician_id}, Patient DOB: {patient_dob}, Status: {status}"+"\n"+
                    f", Summary: {summary},"+"\n"+
                    f"Created At: {created_at}, Updated At: {updated_at}")
        return new_patient_case
        
    


    @exception_handling
    def fetch_by_patient_case_id(self, patient_case_id):
        patient_case = self.session.query(PatientCase).filter(PatientCase.id == patient_case_id).first()
        if not patient_case:
            st.error(f"Patient case with ID {patient_case_id} does not exist.")
            logger.warning(f"Patient case with ID {patient_case_id} does not exist.")
            
        else:
            df = pd.DataFrame([{
                "ID": patient_case.id,
                "Health Center ID": patient_case.health_center_id,
                "Clinician ID": patient_case.clinician_id,
                "Patient Name": patient_case.patient_name,
                "Patient DOB": patient_case.patient_dob,
                "Summary": patient_case.summary,
                "Status": patient_case.status,
                "Created At": patient_case.created_at,
                "Updated At": patient_case.updated_at
            }])
            table = [[patient_case.id, patient_case.health_center_id, patient_case.clinician_id, patient_case.patient_name, patient_case.patient_dob, patient_case.summary, patient_case.status, patient_case.created_at, patient_case.updated_at] for patient_case in [patient_case]]
            st.success(f"Fetched Patient Case ID {patient_case_id} successfully.")
            st.table(df)
            logger.info(f"Fetched patient case by ID {patient_case_id} :- "
                        +"\n" + tabulate(
                            table,
                            headers=["ID", "Health Center ID", "Clinician ID", "Patient Name", "Patient DOB",  "Summary", "Status", "Created At", "Updated At"],
                            tablefmt="grid"
                    ))
        return patient_case



    @optional_filters(PatientCase, 'status', 'patient_name')
    @exception_handling
    def fetch_patient_cases_by_OptionalFilters(self, status=None, patient_name=None, results=None):
        if status is not None:
            if status.lower() not in ['open', 'closed']:
                st.error("Wrong Status must be either 'open' or 'closed'.")
                logger.warning("Wrong Status must be either 'open' or 'closed'.")
            else:
                status = status.lower()
        table = [[pc.id, pc.health_center_id, pc.clinician_id, pc.patient_name, pc.patient_dob, pc.summary, pc.status, pc.created_at, pc.updated_at] for pc in results]
        st.success(f"Fetched Patient Cases with filters - Status: {status} , Patient Name: {patient_name}")
        df = pd.DataFrame([{
            "ID": pc.id,
            "Health Center ID": pc.health_center_id,
            "Clinician ID": pc.clinician_id,
            "Patient Name": pc.patient_name,
            "Patient DOB": pc.patient_dob,
            "Summary": pc.summary,
            "Status": pc.status,
            "Created At": pc.created_at,
            "Updated At": pc.updated_at
        } for pc in results])
        st.table(df)
        if results:
            logger.info("\n" + tabulate(
                table,
                headers=["ID", "Health Center ID", "Clinician ID", "Patient Name", "Patient DOB",  "Summary", "Status", "Created At", "Updated At"],
                tablefmt="grid"
            ) + "\n")
        else:
            st.error(f"No matching Patient Cases found , with status={status} and patient_name={patient_name}")
            logger.warning(f"No matching Patient Cases found , with status={status} and patient_name={patient_name}")

        return results
    

    @transaction
    def update_patient_case(self, patient_case_id, health_center_id=None, clinician_id=None, patient_name=None, patient_dob=None, summary=None, status=None, created_at=None, updated_at=None):
        patient_case = self.session.query(PatientCase).filter(PatientCase.id == patient_case_id).first()
        if not patient_case:
            raise ValueError(f"Patient case with ID {patient_case_id} does not exist.")

        if patient_name is not None:
            patient_case.patient_name = patient_name
        if health_center_id is not None:
            patient_case.health_center_id = health_center_id
        if patient_dob is not None:
            patient_case.patient_dob = patient_dob
        if summary is not None:
            patient_case.summary = summary
        if status is not None:
            if status.lower() not in ['open', 'closed']:
                raise ValueError("Wrong Status must be either 'open' or 'closed'.")
            else:
                patient_case.status = status.lower()
        if created_at is not None:
            patient_case.created_at = created_at
        if updated_at is not None:
            patient_case.updated_at = updated_at

        df = pd.DataFrame([{
            "ID": patient_case.id,
            "Health Center ID": patient_case.health_center_id,
            "Clinician ID": patient_case.clinician_id,
            "Patient Name": patient_case.patient_name,
            "Patient DOB": patient_case.patient_dob,
            "Summary": patient_case.summary,
            "Status": patient_case.status,
            "Created At": patient_case.created_at,
            "Updated At": patient_case.updated_at
        } for patient_case in [patient_case]])

        st.success(f"Updated Patient Case ID {patient_case_id} successfully.")
        st.table(df)
        
        
        table = [[patient_case.id, patient_case.health_center_id, patient_case.clinician_id, patient_case.patient_name, patient_case.patient_dob, patient_case.summary, patient_case.status, patient_case.created_at, patient_case.updated_at]]
        logger.info(f"Updated patient case ID {patient_case_id} with values: "+ "\n" + tabulate(
            table,
            headers=["ID", "Health Center ID", "Clinician ID", "Patient Name", "Patient DOB",  "Summary", "Status", "Created At", "Updated At"],
            tablefmt="grid"
        ))
        
        return patient_case
    

    @login_role_required
    @transaction
    def delete_patient_case(self, patient_case_id):
        patient_case = self.session.query(PatientCase).filter(PatientCase.id == patient_case_id).first()
        if not patient_case:
            raise ValueError(f"Patient case with ID {patient_case_id} does not exist.")
            
        else:
            self.session.delete(patient_case)
            st.success(f"Deleted Patient Case ID {patient_case_id} successfully.")
            logger.info(f"Deleted patient case with ID {patient_case_id}.")
            return True
        return False
    

