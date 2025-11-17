from ..config import Base, Column, Integer, String, relationship, Boolean, Date

class HealthCenter(Base):
    __tablename__ = "health_centers"
    id = Column(Integer, primary_key=True, autoincrement=True , nullable=False)
    name = Column(String(50), nullable=False) 
    address = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, nullable=False)
    clinician = relationship("Clinician", back_populates="health_center")
    patient_case = relationship("PatientCase", back_populates="health_center")

