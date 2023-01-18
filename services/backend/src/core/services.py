import requests
from src.config import config


class Service:

    @classmethod
    async def hand_search_email(cls, email):  # the process is started in a new thread
        """
        This function receives data about the user's mail,
         at the moment this data is displayed in the console and is not stored in the database

        """
        hand_search_api = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={config.HAND_EMAIL_API}'

        response = requests.get(hand_search_api).json()
        data = response.get('data', None)

        if data:
            status = data.get('status', None)

            if status in ['invalid', 'disposable'] or status is None:
                print("EMAIL-DATA", data)
            elif status in ['valid']:
                print("EMAIL-DATA", data)
