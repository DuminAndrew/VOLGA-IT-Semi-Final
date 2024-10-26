from sqlalchemy import Column, Integer, String
from database import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    contact_phone = Column(String)
    rooms = Column(String)  # Список кабинетов больницы в виде строки
