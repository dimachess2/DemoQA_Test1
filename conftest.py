import time
import pytest
import requests
import uuid

BASE_URL = "https://demoqa.com"
REGISTER_URL = f"{BASE_URL}/Account/v1/User"
USER_AUTHORIZED = f"{BASE_URL}/Account/v1/Authorized"
GENERATE_TOKEN = f"{BASE_URL}/Account/v1/GenerateToken"
USER_LOGIN = f"{BASE_URL}/Account/v1/Login"
DELETE_URL = f"{BASE_URL}/Account/v1/User"
#

@pytest.fixture
def test_user():
    username = f"test_{uuid.uuid4().hex[:6]}"
    password = "Qwerty123!"
    payload = {"userName": username, "password": password}

    # 1. Создание пользователя
    reg_response = requests.post(REGISTER_URL, json=payload)
    assert reg_response.status_code == 201, f"Ошибка регистрации: {reg_response.text}"
    user_id = reg_response.json()["userID"]

    # 2. Проверка авторизации
    auth_response = requests.post(USER_AUTHORIZED, json=payload)
    assert auth_response.status_code == 200, f"Ошибка авторизации: {auth_response.text}"

    # 3. Получение токена (первый раз — для тестов)
    token_res = requests.post(GENERATE_TOKEN, json=payload)
    assert token_res.status_code == 200, f'Ошибка получения токена: {token_res.text}'
    token_data = token_res.json()
    assert token_data.get("status") == "Success", f"Токен не активен: {token_data}"
    token = token_data["token"]

    # 4. Логин
    login_response = requests.post(USER_LOGIN, json=payload)
    assert login_response.status_code == 200, f"Ошибка логина: {login_response.text}"

    print(f"[SETUP] Создан пользователь: {username}")
    print(f"User ID: {user_id}")

    # 5. Вывод информации о пользователе
    headers = {"Authorization": f"Bearer {token}"}
    user_info = requests.get(f"{DELETE_URL}/{user_id}", headers=headers)
    print(f"[INFO] Данные о пользователе перед удалением: {user_info.status_code} {user_info.text}")


    yield {
        "username": username,
        "password": password,
        "token": token,
        "user_id": user_id
    }

    # 6. Задержка перед удалением
    time.sleep(2)

    # 7. Повторное получение токена
    token_res = requests.post(GENERATE_TOKEN, json=payload)
    assert token_res.status_code == 200, f'Ошибка получения токена перед удалением: {token_res.text}'
    token_data = token_res.json()
    assert token_data.get("status") == "Success", f"Токен перед удалением не активен: {token_data}"
    delete_token = token_data["token"]

    # 8. Удаление пользователя
    headers = {
        "Authorization": f"Bearer {delete_token}",
        "Content-Type": "application/json"
    }
    delete_url = f"{DELETE_URL}/{user_id}"
    delete_response = requests.delete(delete_url, headers=headers)
    print(f"[DELETE] Ответ: {delete_response.status_code} {delete_response.text}")
    assert delete_response.status_code == 204, f"Ошибка удаления: {delete_response.text}"
    auth_response = requests.post(USER_AUTHORIZED, json=payload)
    assert auth_response.status_code == 404, f"Пользователь не удален: {auth_response.text}"