"""
This module provides a set of FastAPI endpoints for managing users, companies, vacancies, resumes, and submissions. 
It connects to a SQLite database and uses SQLAlchemy for database operations, and Pydantic for data validation 
and serialization.
 
Endpoints:
    - Users:
        POST /users/:
            Create a new user.
        GET /users/:
            Retrieve a list of users with pagination.
        GET /users/{user_id}:
            Retrieve a single user by its ID.
 
    - Companies:
        POST /companies/:
            Create a new company.
        GET /companies/:
            Retrieve a list of companies with pagination.
        GET /companies/{company_id}:
            Retrieve a single company by its ID.
 
    - Vacancies:
        POST /vacancies/:
            Create a new vacancy.
        GET /vacancies/:
            Retrieve a list of vacancies with pagination.
        GET /vacancies/{vacancy_id}:
            Retrieve a single vacancy by its ID.
 
    - Resumes:
        POST /resumes/:
            Create a new resume.
        GET /resumes/:
            Retrieve a list of resumes with pagination.
        GET /resumes/{resume_id}:
            Retrieve a single resume by its ID.
 
    - Submissions:
        POST /submissions/:
            Create a new submission.
        GET /submissions/:
            Retrieve a list of submissions with pagination.
        GET /submissions/{submission_id}:
            Retrieve a single submission by its ID.
 
Models:
    - UserCreate, UserResponse: Validate and represent user data.
    - CompanyCreate, CompanyResponse: Validate and represent company data.
    - VacancyCreate, VacancyResponse: Validate and represent vacancy data.
    - ResumeCreate, ResumeResponse: Validate and represent resume data.
    - SubmissionCreate, SubmissionResponse: Validate and represent submission data.
 
Database:
    - SQLite database accessed via SQLAlchemy.
    - Session management handled by FastAPI dependency injection.
 
Error Handling:
    - Raises HTTPException with appropriate status codes if entities are not found or if errors occur during creation.
 
Logging:
    - Uses the logging library to log information, warnings, and errors related to data operations.
"""
 
import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from columns import Base, User, Company, Vacancy, Resume, Submission
 
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
# Создание базы данных
DATABASE_URL = 'sqlite:///myDatabase.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
app = FastAPI()
 
def get_db():
    """
    Provides a database session to path operations.
 
    Yields:
        Session: A SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
# Модели для валидации данных
class UserCreate(BaseModel):
    """
    Model for creating a new user.
 
    Attributes:
        name (dict): The user's name details.
        email (dict): The user's email details.
        phone (Optional[int]): The user's phone number, if available.
    """
    name: dict
    email: dict
    phone: Optional[int] = None
 
class UserResponse(UserCreate):
    """
    Model for returning user information.
 
    Attributes:
        user_id (int): The unique identifier of the user.
        created_at (datetime): The timestamp when the user was created.
 
    Config:
        orm_mode (bool): Enables compatibility with ORM models.
    """
    user_id: int
    created_at: datetime
 
    class Config:
        orm_mode = True
 
class CompanyCreate(BaseModel):
    """
    Model for creating a new company.
 
    Attributes:
        company_title (dict): The title/name of the company.
        phone (Optional[int]): The company's phone number, if available.
        email (dict): The company's email details.
        company_type (dict): The type or category of the company.
        description (dict): The description of the company.
        website (dict): The company's website details.
    """
    company_title: dict
    phone: Optional[int] = None
    email: dict
    company_type: dict
    description: dict
    website: dict
 
class CompanyResponse(CompanyCreate):
    """
    Model for returning company information.
 
    Attributes:
        company_id (int): The unique identifier of the company.
        created_at (datetime): The timestamp when the company was created.
 
    Config:
        orm_mode (bool): Enables compatibility with ORM models.
    """
    company_id: int
    created_at: datetime
 
    class Config:
        orm_mode = True
 
class VacancyCreate(BaseModel):
    """
    Model for creating a new vacancy.
 
    Attributes:
        company_id (int): The ID of the company posting the vacancy.
        job_title (dict): The title of the vacancy (job position).
        response_letter_required (bool): Whether a response letter is required.
        country (dict): The country where the job is located.
        city (dict): The city where the job is located.
        district (dict): The district where the job is located.
        salary (Optional[int]): The salary offered for the job.
        office_address (dict): The office address for the job location.
        subway_station (dict): The nearest subway station.
        employer_information (dict): Information about the employer.
        requirements (dict): The requirements for the position.
        work_schedule_working (int): The number of working days.
        work_schedule_weekend (int): The number of weekend days.
        experience (dict): The experience required for the position.
        remote_work (bool): Whether remote work is possible.
    """
    company_id: int
    job_title: dict
    response_letter_required: bool
    country: dict
    city: dict
    district: dict
    salary: Optional[int] = None
    office_address: dict
    subway_station: dict
    employer_information: dict
    requirements: dict
    work_schedule_working: int
    work_schedule_weekend: int
    experience: dict
    remote_work: bool
 
class VacancyResponse(VacancyCreate):
    """
    Model for returning vacancy information.
 
    Attributes:
        vacancy_id (int): The unique identifier of the vacancy.
        created_at (datetime): The timestamp when the vacancy was created.
 
    Config:
        orm_mode (bool): Enables compatibility with ORM models.
    """
    vacancy_id: int
    created_at: datetime
 
    class Config:
        orm_mode = True
 
class ResumeCreate(BaseModel):
    """
    Model for creating a new resume.
 
    Attributes:
        user_id (int): The ID of the user who owns the resume.
        title (dict): The title of the resume.
        job_title (dict): The job title the user is applying for.
        country (dict): The country where the user wants to work.
        city (dict): The city where the user wants to work.
        district (dict): The district where the user wants to work.
        min_salary (Optional[int]): The minimum desired salary.
        max_salary (Optional[int]): The maximum desired salary.
        work_schedule_working (int): The working schedule in terms of work days.
        work_schedule_weekend (int): The working schedule in terms of weekend days.
        experience (dict): The user's experience details.
        remote_work (bool): Whether the user is open to remote work.
        education (dict): The user's education details.
        additional_information (dict): Additional details related to the resume.
    """
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
    """
    Model for returning resume information.
 
    Attributes:
        resume_id (int): The unique identifier of the resume.
        created_at (datetime): The timestamp when the resume was created.
 
    Config:
        orm_mode (bool): Enables compatibility with ORM models.
    """
    resume_id: int
    created_at: datetime
 
    class Config:
        orm_mode = True
 
class SubmissionCreate(BaseModel):
    """
    Model for creating a new submission.
 
    Attributes:
        resume_id (int): The ID of the resume being submitted.
        status (dict): The status of the submission.
        sent_at (datetime): The timestamp when the submission was sent.
        vacancy_id (int): The ID of the vacancy for which the resume is being submitted.
    """
    resume_id: int
    status: dict
    sent_at: datetime
    vacancy_id: int
 
class SubmissionResponse(SubmissionCreate):
    """
    Model for returning submission information.
 
    Attributes:
        submission_id (int): The unique identifier of the submission.
        created_at (datetime): The timestamp when the submission was created.
 
    Config:
        orm_mode (bool): Enables compatibility with ORM models.
    """
    submission_id: int
    created_at: datetime
 
    class Config:
        orm_mode = True
 
# CRUD операции для User
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
 
    Args:
        user (UserCreate): The user information to create.
        db (Session): Database session.
 
    Returns:
        UserResponse: The newly created user details.
    """
    logger.info("Creating user with email: %s", user.email)
 
    db_user = User(**user.dict())
 
    db.add(db_user)
 
    try:
        db.commit()
        db.refresh(db_user)
        logger.info("User created successfully with ID: %d", db_user.user_id)
        return db_user
    except Exception as e:
        logger.error("Error creating user: %s", e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating user")
 
@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of users with pagination.
 
    Args:
        skip (int): Number of users to skip.
        limit (int): Maximum number of users to return.
        db (Session): Database session.
 
    Returns:
        List[UserResponse]: A list of user details.
    """
    logger.info("Fetching users with skip=%d and limit=%d", skip, limit)
 
    users = db.query(User).offset(skip).limit(limit).all()
 
    logger.info("Fetched %d users", len(users))
 
    return users
 
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.
 
    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): Database session.
 
    Returns:
        UserResponse: The user details.
 
    Raises:
        HTTPException: If the user is not found.
    """
    logger.info("Fetching user with ID: %d", user_id)
 
    user = db.query(User).filter(User.user_id == user_id).first()
 
    if user is None:
        logger.warning("User not found with ID: %d", user_id)
        raise HTTPException(status_code=404, detail="User not found")
 
    logger.info("Fetched user with ID: %d", user.user_id)
 
    return user
 
# CRUD операции для Company
@app.post("/companies/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """
    Create a new company.
 
    Args:
        company (CompanyCreate): The company information to create.
        db (Session): Database session.
 
    Returns:
        CompanyResponse: The newly created company details.
    """
    logger.info("Creating company with title: %s", company.company_title)
 
    db_company = Company(**company.dict())
 
    db.add(db_company)
 
    try:
        db.commit()
        db.refresh(db_company)
        logger.info("Company created successfully with ID: %d", db_company.company_id)
        return db_company
    except Exception as e:
        logger.error("Error creating company: %s", e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating company")
 
@app.get("/companies/", response_model=List[CompanyResponse])
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of companies with pagination.
 
    Args:
        skip (int): Number of companies to skip.
        limit (int): Maximum number of companies to return.
        db (Session): Database session.
 
    Returns:
        List[CompanyResponse]: A list of company details.
    """
    logger.info("Fetching companies with skip=%d and limit=%d", skip, limit)
 
    companies = db.query(Company).offset(skip).limit(limit).all()
 
    logger.info("Fetched %d companies", len(companies))
 
    return companies
 
@app.get("/companies/{company_id}", response_model=CompanyResponse)
def read_company(company_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single company by ID.
 
    Args:
        company_id (int): The ID of the company to retrieve.
        db (Session): Database session.
 
    Returns:
        CompanyResponse: The company details.
 
    Raises:
        HTTPException: If the company is not found.
    """
    logger.info("Fetching company with ID: %d", company_id)
 
    company = db.query(Company).filter(Company.company_id == company_id).first()
 
    if company is None:
        logger.warning("Company not found with ID: %d", company_id)
        raise HTTPException(status_code=404, detail="Company not found")
 
    logger.info("Fetched company with ID: %d", company.company_id)
 
    return company
 
# CRUD операции для Vacancy
@app.post("/vacancies/", response_model=VacancyResponse)
def create_vacancy(vacancy: VacancyCreate, db: Session = Depends(get_db)):
    """
    Create a new vacancy.
 
    Args:
        vacancy (VacancyCreate): The vacancy information to create.
        db (Session): Database session.
 
    Returns:
        VacancyResponse: The newly created vacancy details.
    """
    logger.info("Creating vacancy: %s", vacancy)
    db_vacancy = Vacancy(**vacancy.dict())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    logger.info("Vacancy created with ID: %d", db_vacancy.vacancy_id)
    return db_vacancy
 
@app.get("/vacancies/", response_model=List[VacancyResponse])
def read_vacancies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of vacancies with pagination.
 
    Args:
        skip (int): Number of vacancies to skip.
        limit (int): Maximum number of vacancies to return.
        db (Session): Database session.
 
    Returns:
        List[VacancyResponse]: A list of vacancy details.
    """
    logger.info("Fetching vacancies with skip=%d and limit=%d", skip, limit)
    vacancies = db.query(Vacancy).offset(skip).limit(limit).all()
    logger.info("Fetched %d vacancies", len(vacancies))
    return vacancies
 
@app.get("/vacancies/{vacancy_id}", response_model=VacancyResponse)
def read_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single vacancy by ID.
 
    Args:
        vacancy_id (int): The ID of the vacancy to retrieve.
        db (Session): Database session.
 
    Returns:
        VacancyResponse: The vacancy details.
 
    Raises:
        HTTPException: If the vacancy is not found.
    """
    logger.info("Fetching vacancy with ID: %d", vacancy_id)
    vacancy = db.query(Vacancy).filter(Vacancy.vacancy_id == vacancy_id).first()
 
    if vacancy is None:
        logger.warning("Vacancy not found with ID: %d", vacancy_id)
        raise HTTPException(status_code=404, detail="Vacancy not found")
 
    logger.info("Fetched vacancy with ID: %d", vacancy.vacancy_id)
    return vacancy
 
# CRUD операции для Resume
@app.post("/resumes/", response_model=ResumeResponse)
def create_resume(resume: ResumeCreate, db: Session = Depends(get_db)):
    """
    Create a new resume.
 
    Args:
        resume (ResumeCreate): The resume information to create.
        db (Session): Database session.
 
    Returns:
        ResumeResponse: The newly created resume details.
    """
    logger.info("Creating resume: %s", resume)
    db_resume = Resume(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    logger.info("Resume created with ID: %d", db_resume.resume_id)
    return db_resume
 
@app.get("/resumes/", response_model=List[ResumeResponse])
def read_resumes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of resumes with pagination.
 
    Args:
        skip (int): Number of resumes to skip.
        limit (int): Maximum number of resumes to return.
        db (Session): Database session.
 
    Returns:
        List[ResumeResponse]: A list of resume details.
    """
    logger.info("Fetching resumes with skip=%d and limit=%d", skip, limit)
    resumes = db.query(Resume).offset(skip).limit(limit).all()
    logger.info("Fetched %d resumes", len(resumes))
    return resumes
 
@app.get("/resumes/{resume_id}", response_model=ResumeResponse)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single resume by ID.
 
    Args:
        resume_id (int): The ID of the resume to retrieve.
        db (Session): Database session.
 
    Returns:
        ResumeResponse: The resume details.
 
    Raises:
        HTTPException: If the resume is not found.
    """
    logger.info("Fetching resume with ID: %d", resume_id)
    resume = db.query(Resume).filter(Resume.resume_id == resume_id).first()
 
    if resume is None:
        logger.warning("Resume not found with ID: %d", resume_id)
        raise HTTPException(status_code=404, detail="Resume not found")
 
    logger.info("Fetched resume with ID: %d", resume.resume_id)
    return resume
 
# CRUD операции для Submission
@app.post("/submissions/", response_model=SubmissionResponse)
def create_submission(submission: SubmissionCreate, db: Session = Depends(get_db)):
    """
    Create a new submission.
 
    Args:
        submission (SubmissionCreate): The submission information to create.
        db (Session): Database session.
 
    Returns:
        SubmissionResponse: The newly created submission details.
    """
    logger.info("Creating submission: %s", submission)
    db_submission = Submission(**submission.dict())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    logger.info("Submission created with ID: %d", db_submission.submission_id)
    return db_submission
 
@app.get("/submissions/", response_model=List[SubmissionResponse])
def read_submissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of submissions with pagination.
 
    Args:
        skip (int): Number of submissions to skip.
        limit (int): Maximum number of submissions to return.
        db (Session): Database session.
 
    Returns:
        List[SubmissionResponse]: A list of submission details.
    """
    logger.info("Fetching submissions with skip=%d and limit=%d", skip, limit)
    submissions = db.query(Submission).offset(skip).limit(limit).all()
    logger.info("Fetched %d submissions", len(submissions))
    return submissions
 
@app.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def read_submission(submission_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single submission by ID.
 
    Args:
        submission_id (int): The ID of the submission to retrieve.
        db (Session): Database session.
 
    Returns:
        SubmissionResponse: The submission details.
 
    Raises:
        HTTPException: If the submission is not found.
    """
    logger.info("Fetching submission with ID: %d", submission_id)
    submission = db.query(Submission).filter(Submission.submission_id == submission_id).first()
 
    if submission is None:
        logger.warning("Submission not found with ID: %d", submission_id)
        raise HTTPException(status_code=404, detail="Submission not found")
 
    logger.info("Fetched submission with ID: %d", submission.submission_id)
    return submission
