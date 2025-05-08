import requests
import json


def create_hh_resume_profile(code, resume_data):
    url = "https://api.hh.ru/resume_profile"
    headers = {
        "Authorization": f"Bearer USERJQJJ7U603ET47P6RPMQP1URHAOOESRK82UI692UGB0UAE87PJCHS4GQUOAHM",
        "Content-Type": "application/json",
        "HH-User-Agent": "YourJobOffer_1 (shirokoriad.ao@phystech.edu)"
    }

    response = requests.post(url, headers=headers, json=resume_data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create resume profile: {response.status_code} {response.text}")


resume_example = {
    'first_name': 'Ксения',
    'last_name': 'Трофимова',
    'citizenship': [
        {
            'id': '113'
        }
    ],
    'area': {
        'id': '2064'
    },
    'language': [
        {
            'id': 'rus',
            'name': 'Русский',
            'level': {
                'id': 'l1',
                'name': 'Родной'
            }
        }
    ],
    'gender': {
        'id': 'female'
    },
    'education': {
        'level': {
            'id': 'higher'
        },
        'primary': [
            {
                'name': 'МФТИ',
                "year": 2028
            }
        ]
    },
    'experience': [
        {
            'company': 'Учебный проект',
            'position': 'Младший разработчик',
            'start': '2024-09-01',
            'description': 'Разработка и поддержка веб-приложений.'
        }
    ],
    'professional_roles': [
        {
            'id': '114',
        }
    ]
}

try:
    result = create_hh_resume_profile("", resume_example)
    resume_id = result['resume']['id']
    print(resume_id)

    headers = {
        "Authorization": f"Bearer USERMBQRQ10VMLQ52PCDG5U323JU4CGICKCDOON1JSIG6T30O7I6L69A1MG4MLN4",
        "HH-User-Agent": "YourJobOffer_1 (shirokoriad.ao@phystech.edu)"
    }

    url = f"https://api.hh.ru/resumes/{resume_id}/publish"
    response = requests.post(url, headers=headers)
    print(response.status_code, response.text)
    print("Created resume profile:", result)
except Exception as e:
    print(e)

print(requests.get("https://api.hh.ru/professional_roles").json())


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


##apply_for_vacancy("USERMBQRQ10VMLQ52PCDG5U323JU4CGICKCDOON1JSIG6T30O7I6L69A1MG4MLN4",
##                  "4eddd0aaff0ec9d89e0039ed1f72534161754d", 119651270, "")
## 2532ac0eff0ecbb20b0039ed1f665a6e657a6d


headers = {
    "Authorization": f"Bearer USERMBQRQ10VMLQ52PCDG5U323JU4CGICKCDOON1JSIG6T30O7I6L69A1MG4MLN4",
    "HH-User-Agent": "YourJobOffer_1 (shirokoriad.ao@phystech.edu)"
}
resume_id = "f5b5a320ff0ecc77cf0039ed1f495461565a50"


def update_resume(token, resume_id, professional_roles):
    url = f"https://api.hh.ru/resumes/{resume_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Данные для обновления
    data = {
        "professional_roles": professional_roles
    }

    response = requests.patch(url, headers=headers, data=data)

    if response.status_code == 204:
        print("Резюме успешно обновлено.")
        return response.json()
    else:
        print(f"Ошибка при обновлении резюме: {response.status_code} {response.text}")
        return None

professional_roles = [
    {
        "id": "8",
        "name": "Администратор"
    }
]

token = "USERMBQRQ10VMLQ52PCDG5U323JU4CGICKCDOON1JSIG6T30O7I6L69A1MG4MLN4"
update_response = update_resume(token, resume_id, professional_roles)
if update_response:
    print("Ответ API:", update_response)


url = f"https://api.hh.ru/resumes/{resume_id}/publish"
response = requests.post(url, headers=headers)
print(response.status_code, response.text)
