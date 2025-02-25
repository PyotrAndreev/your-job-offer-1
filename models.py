from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey, JSON, create_engine, ARRAY
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

# Создание базового класса для моделей
Base = declarative_base()

# Определение URL базы данных
DATABASE_URL = 'sqlite:///myDatabase_mini.db'
engine = create_engine(DATABASE_URL)

class User(Base):
    __tablename__ = 'user'

    user_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    resumes = relationship("Resume", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.name}, email={self.email}, phone={self.phone}, created_at={self.created_at})>"

class Company(Base):
    __tablename__ = 'company'

    company_id = Column(BigInteger, primary_key=True)
    company_title = Column(String)
    phone = Column(BigInteger)  # Контактный номер
    email = Column(String)  # Контактный email
    company_type = Column(String)
    description = Column(String)
    website = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    # vacancies = relationship("Vacancy", back_populates="company")

    def __repr__(self):
        return f"<Company(company_id={self.company_id}, company_title={self.company_title}, phone={self.phone}, email={self.email}, created_at={self.created_at})>"

class Vacancy(Base):
    __tablename__ = 'vacancy'

    vacancy_id = Column(BigInteger, primary_key=True)
    vacancy_id_in_agregator = Column(BigInteger)
    company_id = Column(BigInteger, ForeignKey('company.company_id'))
    job_title = Column(String)
    response_letter_required = Column(Boolean)
    country = Column(String)
    city = Column(String)
    district = Column(String)
    salary = Column(String)
    office_address = Column(String)
    subway_station = Column(String)
    employer_information = Column(String)
    requirements = Column(String)
    work_schedule_working_days = Column(String)
    work_schedule_time_intervals = Column(String)
    experience = Column(String)
    remote_work = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    # company = relationship("Company", back_populates="vacancies")
    submissions = relationship("Submission", back_populates="vacancy")

    def __repr__(self):
        return f"<Vacancy(vacancy_id={self.vacancy_id}, job_title={self.job_title}, salary={self.salary}, company_id={self.company_id}, created_at={self.created_at})>"

class Resume(Base):
    __tablename__ = 'resume'

    resume_id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id'))
    title = Column(String)
    job_title = Column(String)
    country = Column(String)
    city = Column(String)
    district = Column(JSON)
    min_salary = Column(BigInteger)
    max_salary = Column(BigInteger)
    work_schedule_working_days = Column(String)
    work_schedule_time_intervals = Column(String)
    experience = Column(String)
    remote_work = Column(Boolean)
    education = Column(String)
    additional_information = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    user = relationship("User", back_populates="resumes")
    submissions = relationship("Submission", back_populates="resume")

    def __repr__(self):
        return f"<Resume(resume_id={self.resume_id}, title={self.title}, job_title={self.job_title}, user_id={self.user_id}, created_at={self.created_at})>"

class Submission(Base):
    __tablename__ = 'submission'
    submission_id = Column(BigInteger, primary_key=True)
    resume_id = Column(BigInteger, ForeignKey('resume.resume_id'))
    status = Column(String)
    sent_at = Column(DateTime)
    vacancy_id = Column(BigInteger, ForeignKey('vacancy.vacancy_id'))
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    resume = relationship("Resume", back_populates="submissions")
    vacancy = relationship("Vacancy", back_populates="submissions")

    def __repr__(self):
        return f"<Submission(submission_id={self.submission_id}, resume_id={self.resume_id}, vacancy_id={self.vacancy_id}, status={self.status}, created_at={self.created_at})>"

# Создание всех таблиц
Base.metadata.create_all(engine)
