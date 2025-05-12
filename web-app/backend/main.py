import os
from fastapi import FastAPI, Depends, HTTPException, File, Form, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from dotenv import load_dotenv
from pydantic import BaseModel
from uuid import uuid4
from pathlib import Path
from passlib.context import CryptContext

load_dotenv()

# Secure Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Config
class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY")

@AuthJWT.load_config
def get_config():
    return Settings()

app = FastAPI()

baseURL = os.getenv("BASE_URL")

# CORS Configuration (restrict origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL put it in .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTENSIONS = {'pdf'}

from services.hhru_api import exchange_code_for_tokens

class CodeExchangeRequest(BaseModel):
    code: str
    user_id: str

@app.post("/exchange")
def exchange_code(data: CodeExchangeRequest):
    user_id = data.user_id
    code = data.code

    access_token, refresh_token, response = exchange_code_for_tokens(code)

    if access_token is None or refresh_token is None:
        raise HTTPException(status_code=400, detail=("Ошибка при обмене authorization_code" + str(response)))

    add_tokens(user_id, refresh_token, access_token)

    return {"message": "Tokens exchanged successfully"}

from services.new_matcher import search_vacancies_for_user
from database.db_functions import get_hh_access_token, create_submission
from services.hhru_api import get_users_last_resume_id, apply_for_vacancy
from datetime import datetime

class GetVacancies(BaseModel):
    user_id: str
    number_of_vacancies: str

from database.parser_yjo import run_hh_import

@app.post("/get_vacancies")
def get_vacancies(data: GetVacancies):

    run_hh_import()

    
    user_id = data.user_id
    count_of_vacancies = data.number_of_vacancies
    list_of_best_vacancies = search_vacancies_for_user(user_id, count_of_vacancies)
    job_titles = [lst[2] for lst in list_of_best_vacancies]
    vacancies_id = [lst[3] for lst in list_of_best_vacancies]

    return {"job_titles": job_titles, "vacancies_id": vacancies_id}

class ApplyVacancies(BaseModel):
    user_id: str
    vacancies_id: list

@app.post("/apply_vacancies")
def apply_vacancies(data: ApplyVacancies):
    user_id = data.user_id
    vacancies_id = data.vacancies_id

    access_token = get_hh_access_token(user_id)
    resume_id = get_users_last_resume_id(access_token)

    for vacancy_id in vacancies_id:
        apply_for_vacancy(access_token, resume_id, vacancy_id, "")
        create_submission(resume_id, "started", datetime.now(), vacancy_id)

    return {"message": "Vacancies applied successfully"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename_custom(filename: str) -> str:
    """Sanitize filename to ensure it's safe for use in the file system."""
    return str(Path(filename).name)

def save_file(file: UploadFile, user_id: str):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    filename = secure_filename_custom(file.filename)
    unique_filename = f"{user_id}_{uuid4().hex}_{filename}"
    file_path = UPLOAD_DIR / unique_filename
    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())
    return str(file_path)

from database.db_functions import create_resume, update_user_name, update_user_age, update_user_sex


@app.post("/userData")
async def user_data(
    user_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    # resume: UploadFile = File(...),
    country: str = Form(...),
    city: str = Form(...),
    education: str = Form(...),
    position: str = Form(...),
    experience: str = Form(...),
    skills: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...)
):
    # if resume:
        # True
        # resume_path = save_file(resume, user_id)
        # Add resume parsing function

    update_user_name(user_id, first_name + last_name)
    update_user_age(user_id, age)
    update_user_sex(user_id, gender)

    title = "Специалист"
    district = ""
    min_salary = "200000"
    max_salary = "2000000"
    work_schedule_working_days = "пн вт ср чт пт"
    work_schedule_time_intervals = "8:00 17:00"
    remote_work = True

    create_resume(user_id, title, position, country, city, district, min_salary, max_salary,
                work_schedule_working_days, work_schedule_time_intervals,
                experience, remote_work, education, skills)

    message = "Данные успешно сохранены"

    return {"message": message}


from database.db_functions import get_user_by_mail, delete_user

class LoginData(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(data: LoginData, Authorize: AuthJWT = Depends()):

    email = data.email
    password = data.password

    user_data = get_user_by_mail(email)

    if (user_data == None):
        raise HTTPException(status_code=401, detail="Не верный Eamil или пароль")
    
    password_hash, user_id = user_data.values()

    if not verify_password(password, password_hash):
        raise HTTPException(status_code=401, detail="Не верный Eamil или пароль")
    
    access_token = Authorize.create_access_token(subject=data.email)
    return {"access_token": access_token, "user_id": user_id}


# @app.get("/dashboard")
# async def dashboard(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()
#     current_user = Authorize.get_jwt_subject()
#     return {"logged_in_as": current_user}

@app.get("/")
async def entry():
    return "Server is running"


from database.db_functions import create_user, get_last_user_id, add_tokens
from services.hhru_api import exchange_code_for_tokens


class RegistrationData(BaseModel):
    phoneNumber: str
    email: str
    password: str

@app.post("/registration")
async def registration(data: RegistrationData):
    name = ""
    sex = ""
    age = 0
    email = data.email
    phone = data.phoneNumber
    password_hash = hash_password(data.password)

    try:
        create_user(name, sex, age, email, phone, password_hash)
        user_id = get_last_user_id()
        return {"user_id": user_id}
    except Exception as e:
          raise HTTPException(
            status_code=400,
            detail=f"Не удалось создать пользователя: {str(e)}"
        )