from db_functions import create_user, get_last_user_id, add_tokens
from hhru_api import exchange_code_for_tokens

# передается с фронта
name = "Ivan"
sex = "Male"
age = 42
email = "ivan@mail.ru"
phone = "+7232123456"
password_hash = "ansjwe2djnsjdk"

try:
	create_user(name, sex, age, email, phone, password_hash)	
	user_id = get_last_user_id()
except:
	print("Не удалось создать пользователя")
	
# Пользователь соглашается дать доступ
if (True):
	#передается с фронта
	authorization_code = "some_code"
	access_token, refresh_token = exchange_code_for_tokens(authorization_code)
	
	if (access_token != None and refresh_token != None):
		add_tokens(user_id, refresh_token, access_token)
	else:
		print("Ошибка при обмене authorization_code")
