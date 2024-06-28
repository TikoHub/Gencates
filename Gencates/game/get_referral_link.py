import requests

# Замените <your_token> на ваш токен аутентификации
headers = {
    'Authorization': 'Bearer <your_token>'
}

# Выполняем GET-запрос для получения реферальной ссылки
response = requests.get('http://127.0.0.1:8000/get-referral-link/', headers=headers)
if response.status_code == 200:
    referral_link = response.json().get('referral_link')
    print(f'Referral Link: {referral_link}')
else:
    print('Failed to get referral link:', response.json())
