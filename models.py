from sqlalchemy import Column, JSON, Integer, BigInteger, String, Boolean, DateTime, ForeignKey, JSON, create_engine, ARRAY
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
import json

# Создание базового класса для моделей
Base = declarative_base()

# Определение URL базы данных
DATABASE_URL = 'sqlite:///Database.db'
engine = create_engine(DATABASE_URL)

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    sex = Column(String)
    age = Column(Integer)
    email = Column(String)
    phone = Column(BigInteger)
    token = Column(BigInteger)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)  # Добавлено поле created_at

    resumes = relationship("Resume", back_populates="user")
    tokens = relationship("Tokens", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.name}, sex={self.sex}, age={self.age}, email={self.email}, phone={self.phone}, created_at={self.created_at})>"

class Updates(Base):
    __tablename__ = 'updates'

    update_id = Column(Integer, primary_key=True, autoincrement=True)
    agregator = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Updates(update_id={self.update_id}, agregator={self.agregator}, updated_at={self.updated_at})>"

class Vacancy(Base):
    __tablename__ = 'vacancy'

    vacancy_id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id_in_hh = Column(BigInteger)
    vacancy_id_in_hc = Column(BigInteger)
    vacancy_id_in_sj = Column(BigInteger)
    vacancy_id_in_zp = Column(BigInteger)
    job_title = Column(String)
    response_letter_required = Column(Boolean)
    country = Column(String)
    city = Column(String)
    district = Column(String)
    salary = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    office_address = Column(String)
    subway_station = Column(String)
    employer_information = Column(String)
    requirements = Column(String)
    work_schedule_working_days = Column(String)
    work_schedule_time_intervals = Column(String)
    experience = Column(String)
    remote_work = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="vacancy")

    def __repr__(self):
        return f"<Vacancy(vacancy_id={self.vacancy_id}, job_title={self.job_title}, created_at={self.created_at})>"

class Resume(Base):
    __tablename__ = 'resume'

    resume_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id'))
    title = Column(String)
    job_title = Column(String)
    country = Column(String)
    city = Column(String)
    district = Column(String)
    min_salary = Column(BigInteger)
    max_salary = Column(BigInteger)
    work_schedule_working_days = Column(String)
    work_schedule_time_intervals = Column(String)
    experience = Column(String)
    remote_work = Column(Boolean)
    education = Column(String)
    skills = Column(JSON)
    @property
    def skills_list(self):
        return json.loads(self.skills) if self.skills else []

    @skills_list.setter
    def skills_list(self, value):
        self.skills = json.dumps(value)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    submissions = relationship("Submission", back_populates="resume")

    def __repr__(self):
        return f"<Resume(resume_id={self.resume_id}, title={self.title}, job_title={self.job_title}, user_id={self.user_id}, created_at={self.created_at})>"

class Tokens(Base):
    __tablename__ = 'tokens'

    tokens_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id'))
    refresh_token = Column(String)
    access_token = Column(String)

    user = relationship("User", back_populates="tokens")

    def __repr__(self):
        return f"<Tokens(tokens_id={self.tokens_id}, user_id={self.user_id}, refresh_token={self.refresh_token}, access_token={self.access_token})>"

class Submission(Base):
    __tablename__ = 'submission'
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(BigInteger, ForeignKey('resume.resume_id'))
    status = Column(String)
    sent_at = Column(DateTime)
    vacancy_id = Column(BigInteger, ForeignKey('vacancy.vacancy_id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="submissions")
    vacancy = relationship("Vacancy", back_populates="submissions")

    def __repr__(self):
        return f"<Submission(submission_id={self.submission_id}, resume_id={self.resume_id}, vacancy_id={self.vacancy_id}, status={self.status}, created_at={self.created_at})>"

Base.metadata.create_all(engine)
