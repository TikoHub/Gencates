import requests

# Замените referral_code на фактический код реферала, который вы хотите использовать
referral_code = 'uuid-код-реферала'

registration_data = {
    'referral_code': referral_code
}

# Выполняем POST-запрос для регистрации нового пользователя
response = requests.post('http://127.0.0.1:8000/register/', json=registration_data)
if response.status_code == 200:
    print('User registered successfully')
else:
    print('Registration failed:', response.json())
