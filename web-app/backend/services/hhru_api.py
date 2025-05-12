import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("HH_CLIENT_ID")
client_secret = os.getenv("HH_CLIENT_SECRET")

def exchange_code_for_tokens(authorization_code):
	global client_id, client_secret

	data = {
		"grant_type": "authorization_code",
		"client_id": client_id,
		"client_secret": client_secret,
		"code": authorization_code,
	}

	headers = {
		"HH-User-Agent": "YourJobOffer_1 (shirokoriad.ao@phystech.edu)",
		"Content-Type": "application/x-www-form-urlencoded",
	}

	response = requests.post("https://api.hh.ru/token", data=data, headers=headers)

	if response.status_code == 200:
		tokens = response.json()
		access_token = tokens.get("access_token")
		refresh_token = tokens.get("refresh_token")
	else:
		access_token = None
		refresh_token = None
	return (access_token, refresh_token, response.text)


def exchange_refresh_token_for_tokens(refresh_token):
	global client_id, client_secret

	data = {
		"grant_type": "refresh_token",
		"client_id": client_id,
		"client_secret": client_secret,
		"refresh_token": refresh_token,
		"redirect_uri" : "https://github.com/yn864/your-job-offer.git"
	}

	headers = {
		"HH-User-Agent": "YourJobOffer_1 (shirokoriad.ao@phystech.edu)",
		"Content-Type": "application/x-www-form-urlencoded",
	}

	response = requests.post("https://api.hh.ru/token", data=data, headers=headers)

	if response.status_code == 200:
		tokens = response.json()
		access_token = tokens.get("access_token")
		refresh_token = tokens.get("refresh_token")
	else:
		access_token = None
		refresh_token = None
	return (access_token, refresh_token)


# message - сопроводительное письмо не более 10000 символов
def apply_for_vacancy(access_token, resume_id, vacancy_id, message):
	headers = {
		"HH-User-Agent": "YourJobOffer_1 (shirokoriad.ao@phystech.edu)",
		"Authorization": f"Bearer {access_token}",
	}

	data = {
		"resume_id": resume_id,
		"vacancy_id": vacancy_id,
		"message": message,
	}

	res = requests.post("https://api.hh.ru/negotiations", data=data, headers=headers)

	if res.status_code == 201:
		print(f"Отклик на вакансию c vacancy_id {vacancy_id} по resume_id {resume_id} совершен")
		return True
	elif res.status_code == 303:
		location = res.headers.get("Location")
		if location:
			print("Перейдите на сайт работодателя: " + location)
		else:
			print("Схема отклика без внешнего URL")
		return False
	elif res.status_code == 400:
		print(res.content)
		print("Ошибка в параметрах запроса")
		return False
	elif res.status_code == 403:
		print("Невозможно откликнуться на вакансию")
		return False
	else:
		print("Неизвестная ошибка при отклике")
		return False


def get_users_last_resume_id(access_token):
	headers = {
		"HH-User-Agent": "YourJobOffer_1 (shirokoriad.ao@phystech.edu)",
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json",
	}

	res = requests.get("https://api.hh.ru/resumes/mine", headers=headers)

	if res.status_code == 200:
		data = res.json()
		if data['items']:
			 # Первое возвращаемое - это последнее созданное
			first_resume_id = data['items'][0]['id']
			return(first_resume_id)
	else:
		return None
