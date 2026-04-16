import requests
from dotenv import load_dotenv
import os

load_dotenv()

response = requests.get(
    url="https://openrouter.ai/api/v1/auth/key",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"
    }
)

if response.status_code == 200:
    data = response.json()

    limit = data['data']['limit']
    usage = data['data']['usage']

    if limit is None:
        print("На ключе нет отдельного лимита (используется общий баланс аккаунта).")
    else:
        remaining = limit - usage
        print(f"Остаток на ключе: ${remaining:.4f} (из {limit})")

else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
    
print("limit:", limit)
print("usage:", usage)
print("remaining:", None if limit is None else limit - usage)