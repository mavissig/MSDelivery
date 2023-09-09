import os
import requests
from dotenv import load_dotenv


class Connect:
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/customerorder'
    load_dotenv()
    api_token = os.environ.get('TOKEN')
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    def index(self):
        return requests.get(self.url, headers=self.headers)
