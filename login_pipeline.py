from db_functions import get_user_by_mail_and_pass

# передается с фронта
email = "vasya@mail.ru"
password_hash = "asdszeliboba343ds5fse"

user_id = get_user_by_mail_and_pass(email, password_hash)
if (user_id == None):
	# Передаем фронту ошибку (неверный eamil или пароль)
	print("Не верный Eamil или пароль")
else:
	# Передаем user_id фронтенду
	print(f"Пользователь найден, user_id = {user_id}")
