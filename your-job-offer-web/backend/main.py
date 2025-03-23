# import os
# import json
# from fastapi import FastAPI, Depends, HTTPException, File, Form, UploadFile
# from fastapi.security import OAuth2PasswordRequestForm
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi_jwt_auth import AuthJWT
# from dotenv import load_dotenv
# from pydantic import BaseModel
# from uuid import uuid4
# from pathlib import Path

# load_dotenv()

# class Settings(BaseModel):
#     authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY")

# @AuthJWT.load_config
# def get_config():
#     return Settings()

# app = FastAPI()

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Directory to store uploaded files
# UPLOAD_DIR = Path("uploads")
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# # File to simulate database
# DB_FILE = Path("user_db.json")
# if not DB_FILE.exists():
#     DB_FILE.write_text(json.dumps({}))  # Initialize with an empty JSON object


# # Function to save file to disk
# def save_file(file: UploadFile, file_path: Path):
#     with open(file_path, "wb") as buffer:
#         buffer.write(file.file.read())
#     return file_path


# # Function to load user data from the file
# def load_user_data():
#     with open(DB_FILE, "r") as file:
#         return json.load(file)


# # Function to save user data to the file
# def save_user_data(data):
#     with open(DB_FILE, "w") as file:
#         json.dump(data, file, indent=4)


# @app.post("/userData")
# async def user_data(
#     user_id: str = Form(None),
#     first_name: str = Form(...),
#     last_name: str = Form(...),
#     resume: UploadFile = File(...),
#     country: str = Form(...),
#     city: str = Form(...),
#     education: str = Form(...),
#     position: str = Form(...),
#     experience: str = Form(...),
#     skills: str = Form(...),
#     age: int = Form(...),
#     gender: str = Form(...)
# ):
#     # Load existing user data
#     user_data = load_user_data()

#     if not user_id:
#         # New user creation
#         user_id = str(uuid4())  # Generate new user ID
#         message = "New user created successfully"
#     else:
#         # Update existing user
#         if user_id not in user_data:
#             raise HTTPException(status_code=404, detail="User ID not found")
#         message = "User data updated successfully"

#     # Save the resume file with the user ID as part of the filename
#     resume_filename = f"{user_id}_{resume.filename}"
#     resume_path = UPLOAD_DIR / resume_filename
#     save_file(resume, resume_path)

#     # Update or create the user in the "database"
#     user_data[user_id] = {
#         "first_name": first_name,
#         "last_name": last_name,
#         "resume": str(resume_path),
#         "country": country,
#         "city": city,
#         "education": education,
#         "position": position,
#         "experience": experience,
#         "skills": skills,
#         "age": age,
#         "gender": gender,
#     }
#     save_user_data(user_data)

#     # Return the user ID and success message
#     return {
#         "message": message,
#         "user_id": user_id,
#     }


# # @app.get("/userData/{user_id}")
# # async def get_user_data(user_id: str):
# #     # Load user dataser_data = load_user_data()

# #     # Fetch user data by ID
# #     user_info = user_data.get(user_id)

# #     if not user_info:
# #         raise HTTPException(status_code=404, detail="User not found")

# #     return user_info


# @app.get("/hello")
# async def hello():
#     return "Hello!!"

# @app.post("/registration")
# async def registration():
#     return "registered"

# @app.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends()):
#     username = form_data.username
#     password = form_data.password

#     # Validate username and password (mocked here)
#     if username != "test" or password != "test":
#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     access_token = Authorize.create_access_token(subject=username)
#     return {"access_token": access_token}

# @app.get("/dashboard")
# async def dashboard(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()
#     current_user = Authorize.get_jwt_subject()
#     return {"logged_in_as": current_user}

import os
import json
from fastapi import FastAPI, Depends, HTTPException, File, Form, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from dotenv import load_dotenv
from pydantic import BaseModel
from uuid import uuid4
from pathlib import Path
from passlib.context import CryptContext
from werkzeug.utils import secure_filename
from resume_parser.resume_parse import parse_resume


load_dotenv()

# Secure Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Config
class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY") or "default_secret"

@AuthJWT.load_config
def get_config():
    return Settings()

app = FastAPI()

# CORS Configuration - Replace with your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # replace with frontend server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Simulated user database (Replace with real DB)
fake_users_db = {
    "test": {"username": "test", "hashed_password": hash_password("test")}
}

def save_file(file: UploadFile, user_id: str):
    filename = secure_filename(file.filename)
    unique_filename = f"{user_id}_{uuid4().hex}_{filename}"
    file_path = UPLOAD_DIR / unique_filename
    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())
    return str(file_path)

@app.post("/userData")
async def user_data(
    user_id: str = Form(None),
    first_name: str = Form(...),
    last_name: str = Form(...),
    resume: UploadFile = File(...),
    country: str = Form(...),
    city: str = Form(...),
    education: str = Form(...),
    position: str = Form(...),
    experience: str = Form(...),
    skills: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...)
):
    
    if resume:
        parse_resume(resume)

    if not user_id:
        user_id = str(uuid4())  # New User
        message = "New user created successfully"
    else:
        if user_id not in fake_users_db:
            raise HTTPException(status_code=404, detail="User ID not found")
        message = "User data updated successfully"

    resume_path = save_file(resume, user_id)

    fake_users_db[user_id] = {
        "first_name": first_name,
        "last_name": last_name,
        "resume": resume_path,
        "country": country,
        "city": city,
        "education": education,
        "position": position,
        "experience": experience,
        "skills": skills,
        "age": age,
        "gender": gender,
    }
    return {"message": message, "user_id": user_id}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends()):
    user = fake_users_db.get(form_data.username)

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = Authorize.create_access_token(subject=form_data.username)
    return {"access_token": access_token}

@app.get("/dashboard")
async def dashboard(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"logged_in_as": current_user}

@app.get("/hello")
async def hello():
    return "Hello!!"

@app.post("/registration")
async def registration():
    return "registered"
