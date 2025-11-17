from ..config import Base, Column, Integer, String, ForeignKey, relationship, Date

class CaseNote(Base):
    __tablename__ = "case_notes"
    id = Column(Integer, primary_key=True, autoincrement=True , nullable=False)
    case_id = Column(Integer, ForeignKey("patient_cases.id"), nullable=False)
    clinician_id = Column(Integer, ForeignKey("clinicians.id"), nullable=False)
    note_text = Column(String(200), nullable=False)
    created_at = Column(Date, nullable=False)
    patient_case = relationship("PatientCase", back_populates="case_note")
    clinician = relationship("Clinician", back_populates="case_note")

