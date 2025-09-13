import allure
import pytest
from pages.user_page import User_page
from generators import generate_user_body


class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        user = generate_user_body()
        response = User_page.register(user)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert response_data['user']['email'] == user['email']
        assert response_data['user']['name'] == user['name']

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self):
        user = generate_user_body()
        User_page.register(user)
        response = User_page.register(user)
        assert response.status_code == 403
        assert response.json()['message'] == "User already exists"

    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    @allure.title("Создание без обязательного поля {field}")
    def test_create_user_missing_field(self, field):
        user = generate_user_body()
        del user[field]
        response = User_page.register(user)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"
