from ..models.case_note import CaseNote
from ..config import session
from ..utils.logger import logger
from ..utils.decorators import transaction, exception_handling, expected_integer, optional_filters, login_role_required
from tabulate import tabulate


class CaseNoteService:
    def __init__(self):
        self.session = session


    @transaction
    def add_case_note(self,case_id,clinician_id,note_text,created_at):
        
        new_case_note = CaseNote(
            case_id=case_id,
            clinician_id=clinician_id,
            note_text=str(note_text),
            created_at=created_at,
        )
        session.add(new_case_note)
        logger.info(f"Added new case note for Case ID: {case_id},Clinician ID: {clinician_id}, Note: {note_text}, Created At: {created_at}")
        return new_case_note
    


    @exception_handling
    @expected_integer
    def fetch_by_case_note_id(self, case_note_id):
        case_note = session.query(CaseNote).filter(CaseNote.id == case_note_id).first()
        if not case_note:
            raise ValueError(f"Case note with ID {case_note_id} does not exist.")
        else:
            table = [[case_note.id,case_note.case_id, case_note.clinician_id, case_note.note_text, case_note.created_at] for case_note in [case_note]]
            logger.info(f"Fetched case note by ID {case_note_id} :- "
                        +"\n" + tabulate(
                            table,
                            headers=["ID", "Patient Case ID", "Clinician ID", "Note", "Created At"],
                        tablefmt="grid"
                    ))
        return case_note



    @optional_filters(CaseNote,'case_id','created_at')
    @exception_handling
    def fetch_case_notes_by_OptionalFilters(self, case_id=None, created_at=None, results=None):
        table = [[cn.id, cn.case_id, cn.clinician_id, cn.note_text, cn.created_at] for cn in results]
        if results:
            logger.info("\n" + tabulate(
                table,
                headers=["ID", "PatientCase ID", "Clinician ID", "Note", "Created At"],
                tablefmt="grid"
            ) + "\n")
        else:
            raise ValueError(f"No matching case notes found , with case_id={case_id} and created_at={created_at}")

        return results
    


    @transaction
    def update_case_note(self, case_note_id, case_id=None, clinician_id=None, note_text=None, created_at=None):
        case_note = session.query(CaseNote).filter(CaseNote.id == case_note_id).first()
        if not case_note:
            raise ValueError(f"Case note with ID {case_note_id} does not exist.")

        if case_id is not None:
            case_note.case_id = case_id
        if clinician_id is not None:
            case_note.clinician_id = clinician_id
        if note_text is not None:
            case_note.note_text = note_text
        if created_at is not None:
            case_note.created_at = created_at
        

        table = [[case_note.id, case_note.case_id, case_note.clinician_id, case_note.note_text, case_note.created_at]]
        logger.info(f"Updated case note ID {case_note_id} with values: "+ "\n" + tabulate(
            table,
            headers=["ID", "Case ID", "Clinician ID", "Note", "Created At"],
            tablefmt="grid"
        ))
        
        return case_note
    
    @expected_integer
    @login_role_required
    @transaction
    def delete_case_note(self, case_note_id):
        case_note = session.query(CaseNote).filter(CaseNote.id == case_note_id).first()
        if not case_note:
            raise ValueError(f"Case note with ID {case_note_id} does not exist.")
            
        else:
            session.delete(case_note)
            logger.info(f"Deleted case note with ID {case_note_id}.")
    

