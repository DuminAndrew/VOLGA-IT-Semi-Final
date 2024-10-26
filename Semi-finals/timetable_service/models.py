from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base

class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    from_time = Column(DateTime, nullable=False)
    to_time = Column(DateTime, nullable=False)
    room = Column(String, nullable=False)
