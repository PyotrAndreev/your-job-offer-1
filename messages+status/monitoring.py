import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
import logging
import time

client_id = ""
client_secret = ""
authorization_code = ""

def get_response_status(response_id, access_token):
    url = f'https://api.hh.ru/negotiations/{response_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['state']['name']
    else:
        return response.text

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('messages', mode='w', encoding='utf-8')
logger.addHandler(file_handler)

def get_response_messages(response_id, access_token):
    url = f'https://api.hh.ru/negotiations/{response_id}/messages'
    headers = {'Authorization': f'Bearer {access_token}'}
    page = 0
    retries = 5
    messages = []
    while True:
        params = {
            'page': page,
            'per_page': 20
        }
        try:
            response = requests.get(url, headers=headers, params=params)
        except (Timeout, ConnectionError, ConnectionResetError):
            if retries > 0:
                retries -= 1
                logger.warning("Ошибка соединения, повторная попытка через 20 секунд")
                time.sleep(20)
            else:
                logger.error("Повторное соединение не удалось, переходим к следующему запросу")
                break
        except HTTPError as exc:
            if exc.response.status_code == 429:
                logger.warning("Превышено допустимое число запросов, задержка 20 секунд")
                time.sleep(20)
                continue
            logger.error(f"Ошибка {exc.response.status_code}")
            break
        else:
            if response.status_code == 200:
                for message in response.json()['items']:
                    messages.append((message['text'], message['author']))
            else:
                return response.text
            page += 1
        return messages

def get_responses(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    page = 0
    retries = 5
    while True:
        params = {
            'page': page,
            'per_page': 20
        }
        try:
            response = requests.get('https://api.hh.ru/negotiations', headers=headers, params=params)
        except (Timeout, ConnectionError, ConnectionResetError):
            if retries > 0:
                retries -= 1
                logger.warning("Ошибка соединения, повторная попытка через 20 секунд")
                time.sleep(20)
            else:
                logger.error("Повторное соединение не удалось, переходим к следующему запросу")
                break
        except HTTPError as exc:
            if exc.response.status_code == 429:
                logger.warning("Превышено допустимое число запросов, задержка 20 секунд")
                time.sleep(20)
                continue
            logger.error(f"Ошибка {exc.response.status_code}")
            break
        else:

            if response.status_code == 200:
                responses = response.json()
                for res in responses['items']:
                    print(res)
            else:
                print(f"Ошибка: {response.status_code} {response.text}")
            page += 1

# took from Andrey's branch

def get_access_and_refresh_tokens(client_id, client_secret, authorization_code):
	data = {
		"grant_type": "authorization_code",
		"client_id": client_id,
		"client_secret": client_secret,
		"code": authorization_code,
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
		print("Access token:", tokens.get("access_token"))
		print("Refresh token:", tokens.get("refresh_token"))
		return {"access_token" : access_token, "refresh_token" : refresh_token}
	else:
		print(f"Ошибка: {response.status_code} {response.text}")
		return None

get_access_and_refresh_tokens(client_id, client_secret, authorization_code)

vacancy_id = '118747689'
response_id = '4433138566'
chat_id = '4445889311'
access_token = ''

#get_responses(access_token)
#print(get_response_status(response_id, access_token))
#print(get_response_messages(response_id, access_token))
