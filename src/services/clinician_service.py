from ..models.clinician import Clinician
from ..config import session
from ..utils.logger import logger
from ..utils.decorators import transaction, exception_handling, expected_integer, optional_filters, login_role_required
from tabulate import tabulate


class ClinicianService:
    def __init__(self):
        self.session = session


    @transaction
    def add_clinician(self,name,health_center_id,email,role,is_active):
        
        new_clinician = Clinician(
            name=str(name),
            health_center_id=health_center_id,
            email=str(email),
            role=str(role),
            is_active=is_active,
        )
        session.add(new_clinician)
        logger.info(f"Added new clinician: {name} , Health Center ID: {health_center_id}, Email: {email}, Role: {role}, is_active: {is_active}")
        return new_clinician
    


    @exception_handling
    @expected_integer
    def fetch_by_clinician_id(self, clinician_id):
        clinician = session.query(Clinician).filter(Clinician.id == clinician_id).first()
        if not clinician:
            raise ValueError(f"Clinician with ID {clinician_id} does not exist.")
        else:
            table = [[clinician.id,clinician.health_center_id, clinician.name, clinician.email, clinician.role, clinician.is_active] for clinician in [clinician]]
            logger.info(f"Fetched clinician by ID {clinician_id} :- "
                        +"\n" + tabulate(
                            table,
                            headers=["ID", "Health Center ID", "Name", "Email", "Role", "Active"],
                        tablefmt="grid"
                    ))
        return clinician



    @optional_filters(Clinician, 'is_active', 'name')
    @exception_handling
    def fetch_clinicians_by_OptionalFilters(self, name=None, is_active=None, results=None):
        table = [[hc.id, hc.health_center_id, hc.name, hc.email, hc.role, hc.is_active] for hc in results]
        if results:
            logger.info("\n" + tabulate(
                table,
                headers=["ID", "Health Center ID", "Name", "Email", "Role", "Active"],
                tablefmt="grid"
            ) + "\n")
        else:
            raise ValueError(f"No matching clinicians found , with is_active={is_active} and name={name}")

        return results
    

    @login_role_required
    @transaction
    def update_clinician(self, clinician_id, name=None, health_center_id=None, email=None, role=None ,is_active=None):
        clinician = session.query(Clinician).filter(Clinician.id == clinician_id).first()
        if not clinician:
            raise ValueError(f"Clinician with ID {clinician_id} does not exist.")

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
        

        table = [[clinician.id, clinician.health_center_id, clinician.name, clinician.email, clinician.role, clinician.is_active]]
        logger.info(f"Updated clinician ID {clinician_id} with values: "+ "\n" + tabulate(
            table,
            headers=["ID", "Health Center ID", "Name", "Email", "Role", "Active"],
            tablefmt="grid"
        ))
        
        return clinician
    
    @expected_integer
    @login_role_required
    @transaction
    def delete_clinician(self, clinician_id):
        clinician = session.query(Clinician).filter(Clinician.id == clinician_id).first()
        if not clinician:
            raise ValueError(f"Clinician with ID {clinician_id} does not exist.")
            
        else:
            session.delete(clinician)
            logger.info(f"Deleted clinician with ID {clinician_id}.")
    

