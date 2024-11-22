from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey, JSON, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

# Создание базового класса для моделей
Base = declarative_base()

# Определение URL базы данных
DATABASE_URL = 'sqlite:///myDatabase.db'
engine = create_engine(DATABASE_URL)

class User(Base):
    __tablename__ = 'user'

    user_id = Column(BigInteger, primary_key=True)
    name = Column(JSON)
    email = Column(JSON)
    phone = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    resumes = relationship("Resume", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.name}, email={self.email}, phone={self.phone}, created_at={self.created_at})>"

class Company(Base):
    __tablename__ = 'company'

    company_id = Column(BigInteger, primary_key=True)
    company_title = Column(JSON)
    phone = Column(BigInteger)  # Контактный номер
    email = Column(JSON)  # Контактный email
    company_type = Column(JSON)
    description = Column(JSON)
    website = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    vacancies = relationship("Vacancy", back_populates="company")

    def __repr__(self):
        return f"<Company(company_id={self.company_id}, company_title={self.company_title}, phone={self.phone}, email={self.email}, created_at={self.created_at})>"

class Vacancy(Base):
    __tablename__ = 'vacancy'

    vacancy_id = Column(BigInteger, primary_key=True)
    company_id = Column(BigInteger, ForeignKey('company.company_id'))
    job_title = Column(JSON)
    response_letter_required = Column(Boolean)
    country = Column(JSON)
    city = Column(JSON)
    district = Column(JSON)
    salary = Column(BigInteger)
    office_address = Column(JSON)
    subway_station = Column(JSON)
    employer_information = Column(JSON)
    requirements = Column(JSON)
    work_schedule_working = Column(BigInteger)
    work_schedule_weekend = Column(BigInteger)
    experience = Column(JSON)
    remote_work = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    company = relationship("Company", back_populates="vacancies")
    submissions = relationship("Submission", back_populates="vacancy")

    def __repr__(self):
        return f"<Vacancy(vacancy_id={self.vacancy_id}, job_title={self.job_title}, salary={self.salary}, company_id={self.company_id}, created_at={self.created_at})>"

class Resume(Base):
    __tablename__ = 'resume'

    resume_id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id'))
    title = Column(JSON)
    job_title = Column(JSON)
    country = Column(JSON)
    city = Column(JSON)
    district = Column(JSON)
    min_salary = Column(BigInteger)
    max_salary = Column(BigInteger)
    work_schedule_working = Column(BigInteger)
    work_schedule_weekend = Column(BigInteger)
    experience = Column(JSON)
    remote_work = Column(Boolean)
    education = Column(JSON)
    additional_information = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    user = relationship("User", back_populates="resumes")
    submissions = relationship("Submission", back_populates="resume")

    def __repr__(self):
        return f"<Resume(resume_id={self.resume_id}, title={self.title}, job_title={self.job_title}, user_id={self.user_id}, created_at={self.created_at})>"

class Submission(Base):
    __tablename__ = 'submission'
    submission_id = Column(BigInteger, primary_key=True)
    resume_id = Column(BigInteger, ForeignKey('resume.resume_id'))
    status = Column(JSON)
    sent_at = Column(DateTime)
    vacancy_id = Column(BigInteger, ForeignKey('vacancy.vacancy_id'))
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    resume = relationship("Resume", back_populates="submissions")
    vacancy = relationship("Vacancy", back_populates="submissions")

    def __repr__(self):
        return f"<Submission(submission_id={self.submission_id}, resume_id={self.resume_id}, vacancy_id={self.vacancy_id}, status={self.status}, created_at={self.created_at})>"

# Создание всех таблиц
Base.metadata.create_all(engine)
