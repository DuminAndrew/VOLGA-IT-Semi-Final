from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class MedicalHistory(Base):
    __tablename__ = "medical_history"

    id = Column(Integer, primary_key=True, index=True)
    pacient_id = Column(Integer, nullable=False)  # ID пациента
    hospital_id = Column(Integer, nullable=False)  # ID больницы
    doctor_id = Column(Integer, nullable=False)  # ID врача
    date = Column(DateTime, nullable=False)  # Дата визита
    room = Column(String, nullable=False)  # Кабинет
    data = Column(String, nullable=False)  # Данные о визите (описание, назначения)
