from src.imports import session,logger,wraps,IntegrityError, OperationalError, DataError, SQLAlchemyError,PatientCase, Clinician, HealthCenter,CaseNote,CaseNoteService,ClinicianService,HealthCenterService,PatientCaseService,Base, engine, login_role_required ,to_datetime,transaction,Base


class All_Services:
    def __init__(self):
        self.session = session

    def create_tables(self):
        try:
            Base.metadata.create_all(engine)
            logger.info("All tables created successfully.")
        except Exception as e:
            raise e


    def drop_tables(self):
        try:
            Base.metadata.drop_all(engine)
            logger.info("All tables dropped successfully.")
        except Exception as e:
            raise e
        logger.info("All tables dropped successfully.")


    @login_role_required
    @transaction
    def admin_operations(self):
        logger.info("Admin has entered the database")
        print("1. Create Tables" + "\n" +
            "2. Drop Tables")
        choice = int(input("Select the operation you want to perform (1-2): "))
        try:
            if choice == 1:
                self.create_tables()
            elif choice == 2:
                self.drop_tables()
        except Exception as e:
            raise e
        
    def to_bool(self,v):
        if v is None:
            return None
        
        v = str(v).strip().lower()
        if v in ("true", "1", "yes", "y"):
            return True
        if v in ("false", "0", "no", "n"):
            return False
        
        raise ValueError("Invalid boolean input")

        


    def main_services(self):
        hc = HealthCenterService()
        pc = PatientCaseService()
        cs = ClinicianService()
        cn = CaseNoteService()

        print("Welcome to Hospital Case Management System")
        print("1. Health Center Services")
        print("2. Clinician Services")
        print("3. Patient Case Services")
        print("4. Case Note Services")
        print("5. Admin Operations")
        choice = int(input("Select the service you want to use (1-5): "))
        try:
            if choice == 1:
                logger.info("You have selected Health Center Services.")
                print("Services:- 1. Add Health Center" +"\n"
                                " 2. Fetch Health Center by ID" +"\n"
                                " 3. Fetch Health Centers by Optional Filters" +"\n"
                                " 4. Update Health Center" +"\n"
                                " 5. Delete Health Center")
                service_choice = int(input("Select the service you want to use (1-5): "))
                if service_choice == 1:
                    hc.add_health_center(name = input("Enter Health Center Name: "), address = input("Enter Address: "), is_active = self.to_bool(input("Is Active (True/False): ")), created_at = to_datetime(input("Enter Established Date (DD-MM-YYYY): "), format="%d-%m-%Y", errors='coerce'))
                elif service_choice == 2:
                    hc.fetch_health_center_by_id(health_center_id = int(input("Enter Health Center ID: ")))
                elif service_choice == 3:
                    print("You can filter by 'name' or 'is_active' status or by both.")
                    hc.fetch_health_centers_by_OptionalFilters(name = input("Enter Health Center Name (or press Enter to skip): ") or None, is_active = self.to_bool(input("Is Active (True/False) (or press Enter to skip): ") or None))
                elif service_choice == 4:
                    hc.update_health_center(health_center_id = int(input("Enter Health Center ID to update: ")), name = input("Enter new Name (or press Enter to skip): ") or None, address = input("Enter new Address (or press Enter to skip): ") or None, is_active = self.to_bool(input("Is Active (True/False) (or press Enter to skip): ") or None))
                elif service_choice == 5:
                    hc.delete_health_center(health_center_id = int(input("Enter Health Center ID to delete: ")))
            elif choice == 3:
                logger.info("You have selected Patient Case Services.")
                print("Services:- 1. Add Patient Case" +"\n"
                                " 2. Fetch Patient Case by ID" +"\n"
                                " 3. Fetch Patient Cases by Optional Filters" +"\n"
                                " 4. Update Patient Case" +"\n"
                                " 5. Delete Patient Case")
                service_choice = int(input("Select the service you want to use (1-5): "))
                if service_choice == 1:
                    pc.add_patient_case(health_center_id = int(input("Enter Health Center ID: ")), clinician_id = int(input("Enter Clinician ID: ")), patient_name = input("Enter Patient Name: "), patient_dob = to_datetime(input("Enter Patient DOB (DD-MM-YYYY): "), format="%d-%m-%Y", errors='coerce'), summary = input("Enter Summary: "), status = input("Enter Status (open/closed): "), created_at = to_datetime(input("Enter Created At (DD-MM-YYYY): "), format="%d-%m-%Y", errors='coerce'), updated_at = to_datetime(input("Enter Updated At (DD-MM-YYYY): "), format="%d-%m-%Y", errors='coerce'))
                elif service_choice == 2:
                    pc.fetch_by_patient_case_id(patient_case_id = int(input("Enter Patient Case ID: ")))
                elif service_choice == 3:
                    print("You can filter by 'status' or 'patient_name' or by both.")
                    pc.fetch_patient_cases_by_OptionalFilters(status = input("Enter Status (open/closed) (or press Enter to skip): ") or None, patient_name = input("Enter Patient Name (or press Enter to skip): ") or None)
                elif service_choice == 4:
                    pc.update_patient_case(patient_case_id = int(input("Enter Patient Case ID to update: ")), health_center_id = input("Enter new Health Center ID (or press Enter to skip): ") or None, clinician_id = input("Enter new Clinician ID (or press Enter to skip): ") or None, patient_name = input("Enter new Patient Name (or press Enter to skip): ") or None, patient_dob = to_datetime(input("Enter new Patient DOB (DD-MM-YYYY) (or press Enter to skip): ") or None, format="%d-%m-%Y", errors='coerce'), summary = input("Enter new Summary (or press Enter to skip): ") or None, status = input("Enter new Status (open/closed) (or press Enter to skip): ") or None, created_at = to_datetime(input("Enter new Created At (DD-MM-YYYY) (or press Enter to skip): ") or None, format="%d-%m-%Y", errors='coerce'), updated_at = to_datetime(input("Enter new Updated At (DD-MM-YYYY) (or press Enter to skip): ") or None, format="%d-%m-%Y", errors='coerce'))
                elif service_choice == 5:
                    pc.delete_patient_case(patient_case_id = int(input("Enter Patient Case ID to delete: ")))
            elif choice == 2:
                logger.info("You have selected Clinician Services.")
                print("Services:- 1. Add Clinician" +"\n"
                                " 2. Fetch Clinician by ID" +"\n"
                                " 3. Fetch Clinicians by Optional Filters" +"\n"
                                " 4. Update Clinician" +"\n"
                                " 5. Delete Clinician")
                service_choice = int(input("Select the service you want to use (1-5): "))
                if service_choice == 1:
                    cs.add_clinician(name = input("Enter Clinician Name: "), health_center_id = int(input("Enter Health Center ID: ")), email = input("Enter Email: "), role = input("Enter Role: "), is_active = self.to_bool(input("Is Active (True/False): "))    )
                elif service_choice == 2:
                    cs.fetch_by_clinician_id(clinician_id = int(input("Enter Clinician ID: ")))
                elif service_choice == 3:
                    print("You can filter by 'name' or 'is_active' status or by both.")
                    cs.fetch_clinicians_by_OptionalFilters(name = input("Enter Clinician Name (or press Enter to skip): ") or None, is_active = self.to_bool(input("Is Active (True/False) (or press Enter to skip): ") or None))
                elif service_choice == 4:
                    cs.update_clinician(clinician_id = int(input("Enter Clinician ID to update: ")), name = input("Enter new Name (or press Enter to skip): ") or None, health_center_id = input("Enter new Health Center ID (or press Enter to skip): ") or None, email = input("Enter new Email (or press Enter to skip): ") or None, role = input("Enter new Role (or press Enter to skip): ") or None , is_active = self.to_bool(input("Is Active (True/False) (or press Enter to skip): ") or None))
                elif service_choice == 5:
                    cs.delete_clinician(clinician_id = int(input("Enter Clinician ID to delete: ")))
            elif choice == 4:
                logger.info("You have selected Case Note Services.")
                print("Services:- 1. Add Case Note" +"\n"
                                " 2. Fetch Case Note by ID" +"\n"
                                " 3. Fetch Case Notes by Optional Filters" +"\n"
                                " 4. Update Case Note" +"\n"
                                " 5. Delete Case Note")
                service_choice = int(input("Select the service you want to use (1-5): "))
                if service_choice == 1:
                    cn.add_case_note(case_id = int(input("Enter Patient Case ID: ")), clinician_id = int(input("Enter Clinician ID: ")), note_text= input("Enter Note: "), created_at = to_datetime(input("Enter Created At (DD-MM-YYYY): "), format="%d-%m-%Y", errors='coerce'))
                elif service_choice == 2:
                    cn.fetch_by_case_note_id(case_note_id = int(input("Enter Case Note ID: ")))
                elif service_choice == 3:
                    print("You can filter by 'case_id' or 'clinician_id' or by both.")
                    cn.fetch_case_notes_by_OptionalFilters(case_id = input("Enter Patient Case ID (or press Enter to skip): ") or None, created_at= to_datetime(input("Enter Created At (DD-MM-YYYY) (or press Enter to skip): ") or None, format="%d-%m-%Y", errors='coerce'))
                elif service_choice == 4:
                    cn.update_case_note(case_note_id = int(input("Enter Case Note ID to update: ")), case_id = input("Enter new Patient Case ID (or press Enter to skip): ") or None, clinician_id = input("Enter new Clinician ID (or press Enter to skip): ") or None, note_text= input("Enter new Note (or press Enter to skip): ") or None, created_at = to_datetime(input("Enter new Created At (DD-MM-YYYY) (or press Enter to skip): ") or None, format="%d-%m-%Y", errors='coerce'))
                elif service_choice == 5:
                    cn.delete_case_note(case_note_id = int(input("Enter Case Note ID to delete: ")))
            elif choice == 5:
                logger.info("You have selected Admin Operations.")
                self.admin_operations()
            else:
                logger.warning("Invalid choice. Please select a valid service (1-5).")
        except Exception as e:
            raise e
        

    
a1 = All_Services()
a1.main_services()



