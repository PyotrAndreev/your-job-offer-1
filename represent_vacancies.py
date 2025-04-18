from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

from new_matcher import search_vacancies_for_user
from models import User

DATABASE_URL = 'sqlite:///Database.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class VacancyResponse(BaseModel):
    vacancy_id: int
    title: str

@app.get("/vacancies/{user_id}", response_model=List[VacancyResponse])
def get_recommended_vacancies_for_user(user_id: int, num_of_vacancies: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    res_vacancies = search_vacancies_for_user(user_id, num_of_vacancies)
    return res_vacancies