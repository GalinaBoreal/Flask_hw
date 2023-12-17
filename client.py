import requests

# Создать объявление
response = requests.post(
    "http://127.0.0.1:5000/advt",
    json={
        "title": "first",
        "description": "A cat in gloves catches no mice.",
        "owner": "Alex"},
)
print(f'Сооздание объявления. Статус: {response.status_code}.\n{response.text}')

# Получить объявление
response = requests.get("http://127.0.0.1:5000/advt/1")
print(f'Получение объявления. Статус: {response.status_code}.\n{response.text}')

# редактирование объявления

response = requests.patch(
    "http://127.0.0.1:5000/advt/1",
    json={
        "title": "first",
        "description": "A watched pot never boils.",
        "owner": "Alex"}
                          )
print(f'Изменение объявления. Статус: {response.status_code}.\n{response.text}')

# Получить объявление
response = requests.get("http://127.0.0.1:5000/advt/1")
print(f'Получение объявления. Статус: {response.status_code}.\n{response.text}')

# удаление объявления
response = requests.delete(
    "http://127.0.0.1:5000/advt/1",
)
print(f'Удаление объявления. Статус: {response.status_code}.\n{response.text}')

# Создать не проходящее валидацию объявление
response = requests.post(
    "http://127.0.0.1:5000/advt",
    json={
        "title": "f",
        "description": "A cat in gloves catches no mice.",
        "owner": "Alex"},
)
print(f'Сооздание объявления с однобуквенным заголовком. '
      f'Статус: {response.status_code}.\n{response.text}')

# Создать не проходящее валидацию объявление
response = requests.post(
    "http://127.0.0.1:5000/advt",
    json={"title": "fi"},
)
print(f'Сооздание объявления без описания. '
      f'Статус: {response.status_code}.\n{response.text}')
