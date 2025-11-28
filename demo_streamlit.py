import streamlit as st
from src.imports import session,logger,wraps,IntegrityError, OperationalError, DataError, SQLAlchemyError,PatientCase, Clinician, HealthCenter,CaseNote,CaseNoteService,ClinicianService,HealthCenterService,PatientCaseService,AdminService,Base, engine, login_role_required,transaction,to_datetime,transaction,Base

hc = HealthCenterService()
pc = PatientCaseService()
cs = ClinicianService()
cn = CaseNoteService()
admin = AdminService()


# Sidebar Navigation

st.sidebar.title("Hospital Case Management")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Health Center Services",
        "Clinician Services",
        "Patient Case Services",
        "Case Note Services",
        "Admin Operations"
    ]
)

# Home Page

if menu == "Home":
    st.title("Hospital Case Management System")
    st.subheader("Welcome!")
    st.write("""
        This system allows you to manage:
        - Health Centers  
        - Clinicians  
        - Patient Cases  
        - Case Notes  
        - Admin Operations  

        Select a module from the left sidebar.
    """)

# Health Center Services
elif menu == "Health Center Services":
    logger.info("You have selected Health Center Services")
    st.title("Health Center Services",help="Manage Health Centers here")
    

    task = st.selectbox(
        "Choose an operation:",
        [
            "Add Health Center",
            "Fetch Health Center by ID",
            "Fetch Health Centers (Optional Filters)",
            "Update Health Center",
            "Delete Health Center"
        ]
    )

    if task == "Add Health Center":
        st.header("Add Health Center")
        name = st.text_input("Name")
        address = st.text_input("Address")
        is_active = st.selectbox("Is Active?", [True, False])
        created_at = st.date_input("Created At",format="DD-MM-YYYY")

        if st.button("Submit") or ("tx_add_health_center" in st.session_state and st.session_state.get("tx_add_health_center") != "done"):
            hc.add_health_center(name=name, address=address, is_active=is_active, created_at=created_at)


    elif task == "Fetch Health Center by ID":
        st.header("Fetch Health Center by ID")
        id_val = st.number_input("Enter ID", min_value=1, step=1)

        if st.button("Fetch"):
            hc.fetch_health_center_by_id(health_center_id=id_val)

    elif task == "Fetch Health Centers (Optional Filters)":
        st.header("Filter Health Centers")
        name_filter = st.text_input("Name (optional),")
        is_active_filter = st.selectbox(
            "Is Active? (optional)",
            [None, True, False]
        )

        if st.button("Search"):
            hc.fetch_health_centers_by_OptionalFilters(
                name=name_filter if name_filter else None,
                is_active=is_active_filter 
            )

    elif task == "Update Health Center":
        st.header("Update Health Center")
        id_val = st.number_input("Enter ID", min_value=1)
        new_name = st.text_input("New Name")
        new_address = st.text_input("New Address")
        new_status = st.selectbox("Is Active?", [True, False, None])

        if st.button("Update") or ("tx_update_health_center" in st.session_state and st.session_state.get("tx_update_health_center") != "done") or ("login_update_health_center" in st.session_state and st.session_state.get("login_update_health_center") in ["ask", "check"]):
            
            name_val = new_name if new_name else None
            address_val = new_address if new_address else None
            
            hc.update_health_center(health_center_id=id_val, name=name_val, address=address_val, is_active=new_status)
    elif task == "Delete Health Center":
        st.header("Delete Health Center")
        id_val = st.number_input("Enter ID to delete", min_value=1)

        if st.button("Delete") or ("tx_delete_health_center" in st.session_state and st.session_state.get("tx_delete_health_center") != "done") or ("login_delete_health_center" in st.session_state and st.session_state.get("login_delete_health_center") in ["ask", "check"]):
            hc.delete_health_center(health_center_id=id_val)



elif menu == "Clinician Services":
    logger.info("You have selected Clinician Services")
    st.title("Clinician Services",help="Manage Clinicians here")

    task = st.selectbox(
        "Choose an operation:",
        [
            "Add Clinician",
            "Fetch Clinician by ID",
            "Fetch Clinicians (Optional Filters)",
            "Update Clinician",
            "Delete Clinician"
        ]
    )

    if task == "Add Clinician":
        st.header("Add Clinician")
        name = st.text_input("Name")
        health_center_id = st.number_input("Health Center ID", min_value=1, step=1)
        email = st.text_input("Email")
        role = st.selectbox("Role", ["Doctor", "Nurse", "Admin", "Staff"])
        is_active = st.selectbox("Is Active?", [True, False])

        if st.button("Submit") or ("tx_add_clinician" in st.session_state and st.session_state.get("tx_add_clinician") != "done"):
            cs.add_clinician(name=name, health_center_id=health_center_id, email=email, role=role, is_active=is_active)
        
    elif task == "Fetch Clinician by ID":
        st.header("Fetch Clinician by ID")
        id_val = st.number_input("Enter ID", min_value=1, step=1)

        if st.button("Fetch"):
            cs.fetch_by_clinician_id(clinician_id=id_val)
    
    elif task == "Fetch Clinicians (Optional Filters)":
        st.header("Filter Clinicians")
        name_filter = st.text_input("Name (optional),")
        is_active_filter = st.selectbox(
            "Is Active? (optional)",
            [None, True, False]
        )
        if st.button("Search"):
            cs.fetch_clinicians_by_OptionalFilters(
                name=name_filter if name_filter else None,
                is_active=is_active_filter 
            )
    
    elif task == "Update Clinician":
        st.header("Update Clinician")
        id_val = st.number_input("Enter ID", min_value=1)
        new_name = st.text_input("New Name")
        new_health_center_id = st.number_input("New Health Center ID", min_value=1, step=1)
        new_email = st.text_input("New Email")
        new_role = st.text_input("New Role")
        new_status = st.selectbox("Is Active?", [True, False, None])

        if st.button("Update") or ("tx_update_clinician" in st.session_state and st.session_state.get("tx_update_clinician") != "done") or ("login_update_clinician" in st.session_state and st.session_state.get("login_update_clinician") in ["ask", "check"]):
            
            name_val = new_name if new_name else None
            health_center_id_val = new_health_center_id if new_health_center_id else None
            email_val = new_email if new_email else None
            role_val = new_role if new_role else None
            
            cs.update_clinician(clinician_id=id_val, name=name_val, health_center_id=health_center_id_val, email=email_val, role=role_val, is_active=new_status)
    
    elif task == "Delete Clinician":
        st.header("Delete Clinician")
        id_val = st.number_input("Enter ID to delete", min_value=1)

        if st.button("Delete") or ("tx_delete_clinician" in st.session_state and st.session_state.get("tx_delete_clinician") != "done") or ("login_delete_clinician" in st.session_state and st.session_state.get("login_delete_clinician") in ["ask", "check"]):
            cs.delete_clinician(clinician_id=id_val)




# Patient Case Services

elif menu == "Patient Case Services":
    st.title(" Patient Case Services")

    task = st.selectbox(
        "Choose an operation:",
        [
            "Add Patient Case",
            "Fetch Patient Case by ID",
            "Fetch Patient Cases (Optional Filters)",
            "Update Patient Case",
            "Delete Patient Case"
        ]
    )

    if task == "Add Patient Case":
        st.header("Add Patient Case")
        name = st.text_input("Patient Name")
        health_center_id = st.number_input("Health Center ID", min_value=1, step=1)
        clinician_id = st.number_input("Clinician ID", min_value=1, step=1)
        patient_dob = st.date_input("Patient DOB",format="DD-MM-YYYY")
        summary = st.text_area("Summary")
        status = st.selectbox("Status", ["open", "closed"])
        created_at = st.date_input("Created At",format="DD-MM-YYYY")
        updated_at = st.date_input("Updated At",format="DD-MM-YYYY")    
        if st.button("Submit") or ("tx_add_patient_case" in st.session_state and st.session_state.get("tx_add_patient_case") != "done"):
            pc.add_patient_case(
                patient_name=name,
                health_center_id=health_center_id,
                clinician_id=clinician_id,
                patient_dob=patient_dob,
                summary=summary,
                status=status,
                created_at=created_at,
                updated_at=updated_at
            )
    elif task == "Fetch Patient Case by ID":
        st.header("Fetch Patient Case by ID")
        id_val = st.number_input("Enter ID", min_value=1, step=1)

        if st.button("Fetch"):
            pc.fetch_by_patient_case_id(patient_case_id=id_val)
    
    elif task == "Fetch Patient Cases (Optional Filters)":
        st.header("Filter Patient Cases")
        status_filter = st.selectbox(
            "Status (optional)",
            [None, "open", "closed"]
        )
        patient_name_filter = st.text_input("Patient Name (optional),")

        if st.button("Search"):
            pc.fetch_patient_cases_by_OptionalFilters(
                status=status_filter if status_filter else None,
                patient_name=patient_name_filter if patient_name_filter else None
            )
    elif task == "Update Patient Case":
        st.header("Update Patient Case")
        id_val = st.number_input("Enter ID", min_value=1)
        new_name = st.text_input("New Patient Name")
        new_health_center_id = st.number_input("New Health Center ID", min_value=1, step=1)
        new_clinician_id = st.number_input("New Clinician ID", min_value=1, step=1)
        new_patient_dob = st.date_input("New Patient DOB",format="DD-MM-YYYY")
        new_summary = st.text_area("New Summary")
        new_status = st.selectbox("Status", ["open", "closed", None])
        new_created_at = st.date_input("New Created At",format="DD-MM-YYYY")
        new_updated_at = st.date_input("New Updated At",format="DD-MM-YYYY")    

        if st.button("Update") or ("tx_update_patient_case" in st.session_state and st.session_state.get("tx_update_patient_case") != "done") or ("login_update_patient_case" in st.session_state and st.session_state.get("login_update_patient_case") in ["ask", "check"]):
            
            name_val = new_name if new_name else None
            health_center_id_val = new_health_center_id if new_health_center_id else None
            clinician_id_val = new_clinician_id if new_clinician_id else None
            patient_dob_val = new_patient_dob if new_patient_dob else None
            summary_val = new_summary if new_summary else None
            created_at_val = new_created_at if new_created_at else None
            updated_at_val = new_updated_at if new_updated_at else None
            
            pc.update_patient_case(
                patient_case_id=id_val,
                patient_name=name_val,
                health_center_id=health_center_id_val,
                clinician_id=clinician_id_val,
                patient_dob=patient_dob_val,
                summary=summary_val,
                status=new_status,
                created_at=created_at_val,
                updated_at=updated_at_val
            )
    elif task == "Delete Patient Case":
        st.header("Delete Patient Case")
        id_val = st.number_input("Enter ID to delete", min_value=1)

        if st.button("Delete") or ("tx_delete_patient_case" in st.session_state and st.session_state.get("tx_delete_patient_case") != "done") or ("login_delete_patient_case" in st.session_state and st.session_state.get("login_delete_patient_case") in ["ask", "check"]):
            pc.delete_patient_case(patient_case_id=id_val)


# Case Note Services

elif menu == "Case Note Services":
    st.title("Case Note Services")

    task = st.selectbox(
        "Choose an operation:",
        [
            "Add Case Note",
            "Fetch Case Note by ID",
            "Fetch Case Notes (Optional Filters)",
            "Update Case Note",
            "Delete Case Note"
        ]
    )

    if task == "Add Case Note":
        st.header("Add Case Note")
        case_id = st.number_input("Patient Case ID", min_value=1, step=1)
        clinician_id = st.number_input("Clinician ID", min_value=1, step=1)
        note_text = st.text_area("Note Text")
        created_at = st.date_input("Created At",format="DD-MM-YYYY")

        if st.button("Submit") or ("tx_add_case_note" in st.session_state and st.session_state.get("tx_add_case_note") != "done"):
            cn.add_case_note(case_id=case_id, clinician_id=clinician_id, note_text=note_text, created_at=created_at)

    elif task == "Fetch Case Note by ID":
        st.header("Fetch Case Note by ID")
        id_val = st.number_input("Enter ID", min_value=1, step=1)

        if st.button("Fetch"):
            cn.fetch_by_case_note_id(case_note_id=id_val)

    elif task == "Fetch Case Notes (Optional Filters)":
        st.header("Filter Case Notes")
        case_id_filter = st.number_input("Patient Case ID (optional)", min_value=0, step=1, value=0)
        created_at_filter = st.date_input("Created At (optional)", value=None)

        if st.button("Search"):
            cn.fetch_case_notes_by_OptionalFilters(
                case_id=case_id_filter if case_id_filter > 0 else None,
                created_at=created_at_filter
            )

    elif task == "Update Case Note":
        st.header("Update Case Note")
        id_val = st.number_input("Enter ID", min_value=1)
        new_case_id = st.number_input("New Patient Case ID", min_value=0, step=1, value=0)
        new_clinician_id = st.number_input("New Clinician ID", min_value=0, step=1, value=0)
        new_note_text = st.text_area("New Note Text")
        new_created_at = st.date_input("New Created At", value=None)

        if st.button("Update") or ("tx_update_case_note" in st.session_state and st.session_state.get("tx_update_case_note") != "done") or ("login_update_case_note" in st.session_state and st.session_state.get("login_update_case_note") in ["ask", "check"]):
            
            case_id_val = new_case_id if new_case_id > 0 else None
            clinician_id_val = new_clinician_id if new_clinician_id > 0 else None
            note_text_val = new_note_text if new_note_text else None
            created_at_val = new_created_at if new_created_at else None
            
            cn.update_case_note(
                case_note_id=id_val,
                case_id=case_id_val,
                clinician_id=clinician_id_val,
                note_text=note_text_val,
                created_at=created_at_val
            )

    elif task == "Delete Case Note":
        st.header("Delete Case Note")
        id_val = st.number_input("Enter ID to delete", min_value=1)

        if st.button("Delete") or ("tx_delete_case_note" in st.session_state and st.session_state.get("tx_delete_case_note") != "done") or ("login_delete_case_note" in st.session_state and st.session_state.get("login_delete_case_note") in ["ask", "check"]):
            cn.delete_case_note(case_note_id=id_val)


# Admin Services

elif menu == "Admin Operations":
    st.title(" Admin Operations")
    task = st.selectbox(
        "Choose admin task:",
        [
            "Create Tables",
            "Drop Tables",
        ]
    )

    if task == "Create Tables":
        if st.button("Create") or ("tx_create_tables" in st.session_state and st.session_state.get("tx_create_tables") != "done") or ("login_create_tables" in st.session_state and st.session_state.get("login_create_tables") in ["ask", "check"]):
            admin.create_tables()

    if task == "Drop Tables":
        if st.button("DROP ALL TABLES") or ("tx_drop_tables" in st.session_state and st.session_state.get("tx_drop_tables") != "done") or ("login_drop_tables" in st.session_state and st.session_state.get("login_drop_tables") in ["ask", "check"]):
            admin.drop_tables()
