from ..models.health_center import HealthCenter
from ..config import session
from ..utils.logger import logger
from ..utils.decorators import transaction, exception_handling, expected_integer, optional_filters, login_role_required
from tabulate import tabulate


class HealthCenterService:
    def __init__(self):
        self.session = session


    @transaction
    def add_health_center(self, name, address, is_active, created_at):

        new_health_center = HealthCenter(
            name=str(name),
            address=str(address),
            is_active=is_active,
            created_at=created_at,
        )
        session.add(new_health_center)
        logger.info(f"Added new health center: {name} , Address: {address}, is_active: {is_active}, created_at: {created_at}")
        return new_health_center
    


    @exception_handling
    @expected_integer
    def fetch_health_center_by_id(self, health_center_id):
        health_center = session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        if not health_center:
            raise ValueError(f"Health center with ID {health_center_id} does not exist.")
        else:
            table = [[health_center.id, health_center.name, health_center.address, health_center.is_active, health_center.created_at] for health_center in [health_center]]
            logger.info(f"Fetched health center by ID {health_center_id} :- "
                        +"\n" + tabulate(
                            table,
                            headers=["ID", "Name", "Address", "Active", "Created At"],
                            tablefmt="grid"
                        ))
        return health_center



    @optional_filters(HealthCenter, 'is_active', 'name')
    @exception_handling
    def fetch_health_centers_by_OptionalFilters(self, name=None, is_active=None, results=None):
        table = [[hc.id, hc.name, hc.address, hc.is_active, hc.created_at] for hc in results]
        if results:
            logger.info("\n" + tabulate(
                table,
                headers=["ID", "Name", "Address", "Active", "Created At"],
                tablefmt="grid"
            ) + "\n")
        else:
            raise ValueError(f"No matching health centers found , with is_active={is_active} and name={name}")  

        return results
    

    @login_role_required
    @transaction
    def update_health_center(self, health_center_id, name=None, address=None, is_active=None):
        health_center = session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        if not health_center:
            raise ValueError(f"Health center with ID {health_center_id} does not exist.")

        if name is not None:
            health_center.name = name
        if address is not None:
            health_center.address = address
        if is_active is not None:
            health_center.is_active = is_active

        table = [[health_center.id, health_center.name, health_center.address, health_center.is_active, health_center.created_at]]
        logger.info(f"Updated health center ID {health_center_id} with values: "+ "\n" + tabulate(
            table,
            headers=["ID", "Name", "Address", "Active", "Created At"],
            tablefmt="grid"
        ))
        
        return health_center
    
    @expected_integer
    @login_role_required
    @transaction
    def delete_health_center(self, health_center_id):
        health_center = session.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        if not health_center:
            raise ValueError(f"Health center with ID {health_center_id} does not exist.")
            
        else:
            session.delete(health_center)
            logger.info(f"Deleted health center with ID {health_center_id}.")
    
