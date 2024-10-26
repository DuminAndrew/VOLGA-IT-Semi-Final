from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import MedicalHistory
from pydantic import BaseModel
from typing import List
from datetime import datetime

document_router = APIRouter()

class HistoryCreate(BaseModel):
    pacient_id: int
    hospital_id: int
    doctor_id: int
    date: datetime
    room: str
    data: str

class HistoryUpdate(BaseModel):
    pacient_id: int
    hospital_id: int
    doctor_id: int
    date: datetime
    room: str
    data: str

@document_router.post("/", response_model=HistoryCreate)
def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    new_history = MedicalHistory(
        pacient_id=history.pacient_id,
        hospital_id=history.hospital_id,
        doctor_id=history.doctor_id,
        date=history.date,
        room=history.room,
        data=history.data
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history

@document_router.get("/Account/{pacient_id}", response_model=List[HistoryCreate])
def get_history_by_pacient(pacient_id: int, db: Session = Depends(get_db)):
    history = db.query(MedicalHistory).filter(MedicalHistory.pacient_id == pacient_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="No history found for the given pacient ID")
    return history

@document_router.get("/{history_id}", response_model=HistoryCreate)
def get_history(history_id: int, db: Session = Depends(get_db)):
    history = db.query(MedicalHistory).filter(MedicalHistory.id == history_id).first()
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history

@document_router.put("/{history_id}", response_model=HistoryUpdate)
def update_history(history_id: int, history: HistoryUpdate, db: Session = Depends(get_db)):
    db_history = db.query(MedicalHistory).filter(MedicalHistory.id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")

    db_history.pacient_id = history.pacient_id
    db_history.hospital_id = history.hospital_id
    db_history.doctor_id = history.doctor_id
    db_history.date = history.date
    db_history.room = history.room
    db_history.data = history.data

    db.commit()
    db.refresh(db_history)
    return db_history

@document_router.delete("/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    db_history = db.query(MedicalHistory).filter(MedicalHistory.id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    
    db.delete(db_history)
    db.commit()
    return {"detail": "History deleted successfully"}
