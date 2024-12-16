# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

import requests

# При условии уже полученных access_token и refresh_token
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


apply_for_vacancy(
	"USERJS524ISR5PSCKVE1KKN6FLNDGL3E1FMUJAP8NKLM07T1OQHC3OPAI72JI3J7", 
	"ef014e54ff0e19365d0039ed1f7139707a384e", 
	"113150389", 
	"JustTry"
)
