from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from uuid import uuid4
from pathlib import Path
from passlib.context import CryptContext
from flask import Flask, redirect, request, session
import requests
from fastapi import FastAPI
from create_users import get_last_tokens_id, add_tokens

load_dotenv()

# Secure Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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



@app.get("/authorize_in_hh")
def authorize_in_hh():
    client_id = "GES2OLI3SIBO9IEP71CQNM9P35M6FRG29SGD1JFICCRI2P2PQD6F5SBFQHLDO3LD"
    # мб надо поправить redirect_uri
    redirect_uri = "http://localhost:5173/callback?code"
    scope = "account"
    auth_url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    return redirect(auth_url)

@app.route("/callback?code")
def callback():
    authorization_code = request.args.get("code")
    if not authorization_code:
        raise HTTPException(status_code=400, detail="Authorization code had not been received")
    data = {
        "grant_type": "authorization_code",
        "client_id": "GES2OLI3SIBO9IEP71CQNM9P35M6FRG29SGD1JFICCRI2P2PQD6F5SBFQHLDO3LD",
        "client_secret": "NV4JTC1JU0IJNQLBEQLSDDSOQ2RSMDFGNA3NI8UNAJT2R7IGUVIPVNELQU5DR8FG",
        # мб надо поправить redirect_uri
        "redirect_uri": "http://localhost:5173/callback",
        "code": authorization_code
    }
    headers = {
        "HH-User-Agent": "YourJobOffer_1 (shirokoriad.ao@phystech.edu)",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    token_response = requests.post("https://api.hh.ru/token", data=data, headers=headers)
    if not token_response.ok:
        raise HTTPException(status_code=500, detail="Error while trying to get tokens: {token_response.text}")
    else:
        token_data = token_response.json()
        session["access_token"] = token_data["access_token"]
        session["refresh_token"] = token_data.get("refresh_token", "")
        # надо как-то вытащить user_id???
        #add_tokens(get_last_tokens_id() + 1, user_id, token_data["access_token"], token_data.get("refresh_token", ""))
        return redirect("/dashboard")

