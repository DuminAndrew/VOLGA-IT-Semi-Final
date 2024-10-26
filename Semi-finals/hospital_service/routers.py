from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Hospital
from pydantic import BaseModel
from typing import List

hospital_router = APIRouter()


class HospitalCreate(BaseModel):
    name: str
    address: str
    contact_phone: str
    rooms: List[str]

class HospitalUpdate(BaseModel):
    name: str
    address: str
    contact_phone: str
    rooms: List[str]

@hospital_router.post("/", response_model=HospitalCreate)
def create_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    new_hospital = Hospital(
        name=hospital.name,
        address=hospital.address,
        contact_phone=hospital.contact_phone,
        rooms=",".join(hospital.rooms)
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return new_hospital

@hospital_router.get("/", response_model=List[HospitalCreate])
def get_hospitals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    hospitals = db.query(Hospital).offset(skip).limit(limit).all()
    return hospitals

@hospital_router.get("/{hospital_id}", response_model=HospitalCreate)
def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@hospital_router.put("/{hospital_id}", response_model=HospitalUpdate)
def update_hospital(hospital_id: int, hospital: HospitalUpdate, db: Session = Depends(get_db)):
    db_hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")

    db_hospital.name = hospital.name
    db_hospital.address = hospital.address
    db_hospital.contact_phone = hospital.contact_phone
    db_hospital.rooms = ",".join(hospital.rooms)

    db.commit()
    db.refresh(db_hospital)
    return db_hospital

@hospital_router.delete("/{hospital_id}")
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    db_hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    db.delete(db_hospital)
    db.commit()
    return {"detail": "Hospital deleted successfully"}
