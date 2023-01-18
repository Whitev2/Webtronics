import requests


def hand_search_email(email):
    api_key = "6fdf1f7637031cb94443c03af55d10a89f5394ed"
    hand_search_api = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}'

    response = requests.get(hand_search_api).json()
    data = response.get('data', None)

    if data:
        status = data.get('status', None)

        if status in ['invalid', 'disposable'] or status is None:
            return None
        elif status in ['valid']:
            return data
