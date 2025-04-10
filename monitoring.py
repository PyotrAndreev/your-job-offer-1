import requests

client_id = "GES2OLI3SIBO9IEP71CQNM9P35M6FRG29SGD1JFICCRI2P2PQD6F5SBFQHLDO3LD"
client_secret = "NV4JTC1JU0IJNQLBEQLSDDSOQ2RSMDFGNA3NI8UNAJT2R7IGUVIPVNELQU5DR8FG"
authorization_code = "UA5HM31PC0CA978HCDRSMRSPJB0GDJVNSF9QMEDHFNN8RUGQJQSRQA2SOFN0FFBD"

def get_response_status(response_id, access_token):
    url = f'https://api.hh.ru/negotiations/{response_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['state']['name']
    else:
        return response.text


def get_response_messages(response_id, access_token):
    url = f'https://api.hh.ru/negotiations/{response_id}/messages'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    messages = []
    if response.status_code == 200:
        for message in response.json()['items']:
            messages.append((message['text'], message['author']))
        return messages
    else:
        return response.text

def get_responses(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.hh.ru/negotiations', headers=headers)

    if response.status_code == 200:
        responses = response.json()
        for res in responses['items']:
            print(res)
    else:
        print(f"Ошибка: {response.status_code} {response.text}")

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

#get_access_and_refresh_tokens(client_id, client_secret, authorization_code)

vacancy_id = '118747689'
response_id = '4433138566'
chat_id = '4445889311'
access_token = 'USERPGVQMKFD1EGAU2LLB43JHD57RAF9J0E1AKONNNA5KSKOAD7SC76A5PAEHD73'

get_responses(access_token)
print(get_response_status(response_id, access_token))
print(get_response_messages(response_id, access_token))
