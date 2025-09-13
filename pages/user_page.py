import json
import requests
from data import Url


class User_page:
    @staticmethod
    def register(body):
        response = requests.post(Url.BASE_URL + Url.REGISTER, json=body)
        if response.status_code == 200 and 'accessToken' in response.json():
            data = response.json()
            if data['accessToken'].startswith('Bearer '):
                data['accessToken'] = data['accessToken'][7:]
            response._content = json.dumps(data).encode()
        return response

    @staticmethod
    def login(body):
        return requests.post(Url.BASE_URL + Url.LOGIN, json=body)

    @staticmethod
    def update_user(token, update_data):
        headers = {
            'Authorization': f'Bearer {token}' if token else None,
            'Content-Type': 'application/json'
        }
        headers = {k: v for k, v in headers.items() if v is not None}

        return requests.patch(
            Url.BASE_URL + Url.USER,
            headers=headers,
            json=update_data
        )

    @staticmethod
    def delete_user(token):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        return requests.delete(Url.BASE_URL + Url.USER, headers=headers)
