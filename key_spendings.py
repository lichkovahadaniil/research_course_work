import os

import requests
from dotenv import load_dotenv


load_dotenv()


def main() -> None:
    response = requests.get(
        url="https://openrouter.ai/api/v1/auth/key",
        headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"},
        timeout=30,
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return

    data = response.json()["data"]
    limit = data.get("limit")
    usage = data.get("usage")
    remaining = None if limit is None or usage is None else limit - usage

    if limit is None:
        print("The key does not have a dedicated limit; it uses the shared account balance.")
    else:
        print(f"Remaining key balance: ${remaining:.4f} (out of {limit})")

    print("limit:", limit)
    print("usage:", usage)
    print("remaining:", remaining)


if __name__ == "__main__":
    main()
