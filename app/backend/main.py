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
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY") or "default_secret"

@AuthJWT.load_config
def get_config():
    return Settings()

app = FastAPI()

# CORS Configuration (restrict origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # Replace with your frontend URL put it in .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Simulated user database
fake_users_db = {
    "test": {"username": "test", "hashed_password": hash_password("test")}
}

ALLOWED_EXTENSIONS = {'pdf'}

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
        True
        # Add resume parsing function

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
async def registration(username: str, password: str):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = hash_password(password)
    fake_users_db[username] = {"username": username, "hashed_password": hashed_password}
    return {"message": "User registered successfully"}
