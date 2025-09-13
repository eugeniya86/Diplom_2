import allure
import pytest
from pages.user_page import User_page
from generators import UserGenerator


class TestUserUpdate:
    @pytest.mark.parametrize("field,value", [
        ("email", UserGenerator.random_email()),
        ("name", "New Name"),
    ])
    @allure.title("Успешное обновление поля {field}")
    def test_successful_update(self, registered_user, field, value):
        token = registered_user['response']['accessToken']
        update = {field: value}
        response = User_page.update_user(token, update)
        assert response.status_code == 200
        assert response.json()["user"][field] == value

    @allure.title("Обновление пароля")
    def test_password_update(self, registered_user, auth_token):
        new_password = UserGenerator.random_password()
        auth_token = registered_user['response']['accessToken']
        response = User_page.update_user(auth_token, {"password": new_password})
        assert response.status_code == 200
        login_response = User_page.login({
            "email": registered_user['data']['email'],
            "password": new_password
        })
        assert login_response.status_code == 200

    @pytest.mark.parametrize("field,value", [
        ("email", "test@test.com"),
        ("password", "qwerty123"),
        ("name", "Tests"),
    ])
    @allure.title(" обновление поля без авторизации")
    def test_update_unauthorized(self, field, value):
        response = User_page.update_user("", {field: value})
        assert response.status_code == 401
        assert response.json()['message'] == "You should be authorised"

    @allure.title("Обновление данных с неверным токеном")
    def test_update_with_invalid_token(self):
        response = User_page.update_user("test", {"name": "Test"})
        assert response.status_code == 403

    @allure.title("Обновление email пустым значением")
    def test_update_empty_email(self, registered_user, auth_token):
        auth_token = registered_user['response']['accessToken']
        response = User_page.update_user(auth_token, {"email": ""})
        assert response.status_code == 403

    @allure.title("Обновление имени пустым значением")
    def test_update_empty_name(self, registered_user, auth_token):
        auth_token = registered_user['response']['accessToken']
        response = User_page.update_user(auth_token, {"name": ""})
        assert response.status_code == 400

    @allure.title("Попытка изменить на существующий email")
    def test_update_to_existing_email(self, registered_user, existing_user):
        response = User_page.update_user(
            registered_user['response']['accessToken'],
            {"email": existing_user['data']['email']}
        )
        assert response.status_code in [403]

    @allure.title("Обновление email существующего пользователя")
    def test_update_existing_user_email(self, registered_user):
        token = registered_user['response']['accessToken']
        original_email = registered_user['data']['email']
        new_email = UserGenerator.random_email()
        update_response = User_page.update_user(token, {"email": new_email})
        assert update_response.status_code == 200
        update = update_response.json()
        assert update["success"] is True
        assert update["user"]["email"] == new_email
        assert update["user"]["name"] == registered_user['data']['name']

        callback = User_page.update_user(token, {"email": original_email})
        assert callback.status_code == 200
        rollback_data = callback.json()
        assert rollback_data["success"] is True
        assert rollback_data["user"]["email"] == original_email
        assert rollback_data["user"]["name"] == registered_user['data']['name']
