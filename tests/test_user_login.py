import allure
import pytest
from pages.user_page import User_page


class TestUserLogin:
    @allure.title("Успешная авторизация с валидными данными")
    def test_login_existing_user(self, registered_user):
        test_user = registered_user['data']
        login_data = {
            "email": test_user['email'],
            "password": test_user['password']
        }
        response = User_page.login(login_data)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert 'user' in response_data
        assert response_data['user']['email'] == test_user['email']
        assert response_data['user']['name'] == test_user['name']

    @allure.title("Неуспешная авторизация с невалидными данными")
    @pytest.mark.parametrize("email, password, expected_message", [
        ("user@yandex.ru", "qwerty", "email or password are incorrect"),
        ("invalid_email_format", "password123", "email or password are incorrect"),
        ("", "qwerty", "email or password are incorrect"),
        ("user@yandex.ru", "", "email or password are incorrect")
    ])
    def test_login_invalid_credentials(self, email, password, expected_message):
        login_data = {
            "email": email,
            "password": password
        }
        response = User_page.login(login_data)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert response_data['message'] == expected_message
