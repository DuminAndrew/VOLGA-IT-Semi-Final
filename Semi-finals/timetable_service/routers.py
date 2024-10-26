from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Timetable
from pydantic import BaseModel
from typing import List
from datetime import datetime

timetable_router = APIRouter()

class TimetableCreate(BaseModel):
    hospital_id: int
    doctor_id: int
    from_time: datetime
    to_time: datetime
    room: str

class TimetableUpdate(BaseModel):
    hospital_id: int
    doctor_id: int
    from_time: datetime
    to_time: datetime
    room: str

@timetable_router.post("/", response_model=TimetableCreate)
def create_timetable(timetable: TimetableCreate, db: Session = Depends(get_db)):
    if timetable.to_time <= timetable.from_time:
        raise HTTPException(status_code=400, detail="'to_time' must be after 'from_time'")
    
    new_timetable = Timetable(
        hospital_id=timetable.hospital_id,
        doctor_id=timetable.doctor_id,
        from_time=timetable.from_time,
        to_time=timetable.to_time,
        room=timetable.room
    )
    db.add(new_timetable)
    db.commit()
    db.refresh(new_timetable)
    return new_timetable

@timetable_router.get("/", response_model=List[TimetableCreate])
def get_timetables(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    timetables = db.query(Timetable).offset(skip).limit(limit).all()
    return timetables

@timetable_router.get("/{timetable_id}", response_model=TimetableCreate)
def get_timetable(timetable_id: int, db: Session = Depends(get_db)):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if timetable is None:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return timetable

@timetable_router.put("/{timetable_id}", response_model=TimetableUpdate)
def update_timetable(timetable_id: int, timetable: TimetableUpdate, db: Session = Depends(get_db)):
    db_timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if db_timetable is None:
        raise HTTPException(status_code=404, detail="Timetable not found")
    
    if timetable.to_time <= timetable.from_time:
        raise HTTPException(status_code=400, detail="'to_time' must be after 'from_time'")

    db_timetable.hospital_id = timetable.hospital_id
    db_timetable.doctor_id = timetable.doctor_id
    db_timetable.from_time = timetable.from_time
    db_timetable.to_time = timetable.to_time
    db_timetable.room = timetable.room

    db.commit()
    db.refresh(db_timetable)
    return db_timetable

@timetable_router.delete("/{timetable_id}")
def delete_timetable(timetable_id: int, db: Session = Depends(get_db)):
    db_timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if db_timetable is None:
        raise HTTPException(status_code=404, detail="Timetable not found")
    
    db.delete(db_timetable)
    db.commit()
    return {"detail": "Timetable deleted successfully"}

@timetable_router.post("/{timetable_id}/Appointments")
def book_appointment(timetable_id: int, time: datetime, db: Session = Depends(get_db)):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if timetable is None:
        raise HTTPException(status_code=404, detail="Timetable not found")
    
    if time < timetable.from_time or time >= timetable.to_time:
        raise HTTPException(status_code=400, detail="Invalid appointment time")
    
    return {"detail": "Appointment booked", "time": time}
