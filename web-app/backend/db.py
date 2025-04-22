from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from matcher import vacancies, match_vacancies
from models import Base, User, Company, Vacancy, Resume, Submission

# Создание базы данных
DATABASE_URL = 'sqlite:///myDatabase_mini.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модели  для валидации данных
class UserCreate(BaseModel):
    name: dict
    email: dict
    phone: Optional[int] = None

class UserResponse(UserCreate):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CompanyCreate(BaseModel):
    company_title: dict
    phone: Optional[int] = None
    email: dict
    company_type: dict
    description: dict
    website: dict

class CompanyResponse(CompanyCreate):
    company_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class VacancyCreate(BaseModel):
    company_id: int
    job_title: dict
    response_letter_required: bool
    country: dict
    city: dict
    district: dict
    salary: list
    office_address: dict
    subway_station: dict
    employer_information: dict
    requirements: dict
    work_schedule_working: int
    work_schedule_weekend: int
    experience: dict
    remote_work: bool

class TokensCreate(BaseModel):
    user_id: int
    refresh_token: str
    access_token: str

class TokensResponse(TokensCreate):
    tokens_id: int

    class Config:
        orm_mode = True

class VacancyResponse(VacancyCreate):
    vacancy_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ResumeCreate(BaseModel):
    user_id: int
    title: dict
    job_title: dict
    country: dict
    city: dict
    district: dict
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    work_schedule_working: int
    work_schedule_weekend: int
    experience: dict
    remote_work: bool
    education: dict
    additional_information: dict

class ResumeResponse(ResumeCreate):
    resume_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SubmissionCreate(BaseModel):
    resume_id: int
    status: dict
    sent_at: datetime
    vacancy_id: int

class SubmissionResponse(SubmissionCreate):
    submission_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# CRUD операции для User
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CRUD операции для Company
@app.post("/companies/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.get("/companies/", response_model=List[CompanyResponse])
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@app.get("/companies/{company_id}", response_model=CompanyResponse)
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.company_id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# CRUD операции для Vacancy
@app.post("/vacancies/", response_model=VacancyResponse)
def create_vacancy(vacancy: VacancyCreate, db: Session = Depends(get_db)):
    db_vacancy = Vacancy(**vacancy.dict())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

@app.get("/vacancies/", response_model=List[VacancyResponse])
def read_vacancies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    vacancies = db.query(Vacancy).offset(skip).limit(limit).all()
    return vacancies

@app.get("/vacancies/{vacancy_id}", response_model=VacancyResponse)
def read_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    vacancy = db.query(Vacancy).filter(Vacancy.vacancy_id == vacancy_id).first()
    if vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy

# CRUD операции для Resume
@app.post("/resumes/", response_model=ResumeResponse)
def create_resume(resume: ResumeCreate, db: Session = Depends(get_db)):
    db_resume = Resume(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

@app.get("/resumes/", response_model=List[ResumeResponse])
def read_resumes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    resumes = db.query(Resume).offset(skip).limit(limit).all()
    return resumes

@app.get("/resumes/{resume_id}", response_model=ResumeResponse)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.resume_id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

# CRUD операции для Submission
@app.post("/submissions/", response_model=SubmissionResponse)
def create_submission(submission: SubmissionCreate, db: Session = Depends(get_db)):
    db_submission = Submission(**submission.dict())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

@app.get("/submissions/", response_model=List[SubmissionResponse])
def read_submissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    submissions = db.query(Submission).offset(skip).limit(limit).all()
    return submissions

@app.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def read_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.submission_id == submission_id).first()
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission

@app.get("/vacancies/{user_id}", response_model=List[VacancyResponse])
def get_recommended_vacancies_for_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    res_vacancies = match_vacancies(vacancies, user_id)
    return res_vacancies

# Запуск приложения можно осуществить с помощью команды:
# uvicorn main:app --reload