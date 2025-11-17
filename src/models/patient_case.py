from ..config import Base, Column, Integer, String, ForeignKey, relationship, Date, CheckConstraint


class PatientCase(Base):
    __tablename__ = "patient_cases"
    id = Column(Integer, primary_key=True, autoincrement=True , nullable=False)
    health_center_id = Column(Integer, ForeignKey("health_centers.id"), nullable=False)
    clinician_id = Column(Integer, ForeignKey("clinicians.id"), nullable=False)
    patient_name = Column(String(50), nullable=False)
    patient_dob = Column(Date, nullable=False)
    summary = Column(String(500), nullable=False)
    status = Column(String(10), CheckConstraint("status IN ('open', 'closed')"), nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=False)
    health_center = relationship("HealthCenter", back_populates="patient_case")
    clinician = relationship("Clinician", back_populates="patient_case")
    case_note = relationship("CaseNote", back_populates="patient_case")

