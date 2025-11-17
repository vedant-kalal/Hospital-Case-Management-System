from ..config import Base, Column, Integer, String, ForeignKey, relationship, Boolean

class Clinician(Base):
    __tablename__ = "clinicians"
    id = Column(Integer, primary_key=True, autoincrement=True , nullable=False)
    health_center_id = Column(Integer, ForeignKey("health_centers.id"), nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    role = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True)
    health_center = relationship("HealthCenter", back_populates="clinician")
    case_note = relationship("CaseNote", back_populates="clinician")
    patient_case = relationship("PatientCase", back_populates="clinician")