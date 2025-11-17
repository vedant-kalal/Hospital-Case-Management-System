from ..models.patient_case import PatientCase
from ..config import session
from ..utils.logger import logger
from ..utils.decorators import transaction, exception_handling, expected_integer, optional_filters, login_role_required
from tabulate import tabulate


class PatientCaseService:
    def __init__(self):
        self.session = session


    @transaction
    def add_patient_case(self, health_center_id, clinician_id, patient_name, patient_dob, summary, status, created_at, updated_at):

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
        session.add(new_patient_case)
        logger.info(f"Added new patient case: {patient_name} , Health Center ID: {health_center_id}, Clinician ID: {clinician_id}, Patient DOB: {patient_dob}, Status: {status}"+"\n"+
                    f", Summary: {summary}"+"\n"+
                    f"Created At: {created_at}, Updated At: {updated_at}")
        return new_patient_case
        
    


    @exception_handling
    @expected_integer
    def fetch_by_patient_case_id(self, patient_case_id):
        patient_case = session.query(PatientCase).filter(PatientCase.id == patient_case_id).first()
        if not patient_case:
            raise ValueError(f"Patient case with ID {patient_case_id} does not exist.")
        else:
            table = [[patient_case.id, patient_case.health_center_id, patient_case.clinician_id, patient_case.patient_name, patient_case.patient_dob, patient_case.summary, patient_case.status, patient_case.created_at, patient_case.updated_at] for patient_case in [patient_case]]
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
                raise ValueError("Wrong Status must be either 'open' or 'closed'.")
            else:
                status = status.lower()
        table = [[pc.id, pc.health_center_id, pc.clinician_id, pc.patient_name, pc.patient_dob, pc.summary, pc.status, pc.created_at, pc.updated_at] for pc in results]
        if results:
            logger.info("\n" + tabulate(
                table,
                headers=["ID", "Health Center ID", "Clinician ID", "Patient Name", "Patient DOB",  "Summary", "Status", "Created At", "Updated At"],
                tablefmt="grid"
            ) + "\n")
        else:
            raise ValueError(f"No matching Patient Cases found , with status={status} and patient_name={patient_name}")

        return results
    

    @transaction
    def update_patient_case(self, patient_case_id, health_center_id=None, clinician_id=None, patient_name=None, patient_dob=None, summary=None, status=None, created_at=None, updated_at=None):
        patient_case = session.query(PatientCase).filter(PatientCase.id == patient_case_id).first()
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
        
        
        table = [[patient_case.id, patient_case.health_center_id, patient_case.clinician_id, patient_case.patient_name, patient_case.patient_dob, patient_case.summary, patient_case.status, patient_case.created_at, patient_case.updated_at]]
        logger.info(f"Updated patient case ID {patient_case_id} with values: "+ "\n" + tabulate(
            table,
            headers=["ID", "Health Center ID", "Clinician ID", "Patient Name", "Patient DOB",  "Summary", "Status", "Created At", "Updated At"],
            tablefmt="grid"
        ))
        
        return patient_case
    
    @expected_integer
    @login_role_required
    @transaction
    def delete_patient_case(self, patient_case_id):
        patient_case = session.query(PatientCase).filter(PatientCase.id == patient_case_id).first()
        if not patient_case:
            raise ValueError(f"Patient case with ID {patient_case_id} does not exist.")
            
        else:
            session.delete(patient_case)
            logger.info(f"Deleted patient case with ID {patient_case_id}.")
    

