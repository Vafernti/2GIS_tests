import allure

from constants import DEFAULT_PAYLOAD, OLD_TOKEN


@allure.feature("POST /v1/auth/tokens")
@allure.story("Проверка получения токена аутентификации")
@allure.tag("positive", "smoke")
def test_get_auth_token(unauth_api):
    resp = unauth_api.get_token()
    assert resp.status_code == 200, f"{resp.status_code} {resp.text}"
    assert "token" in resp.cookies, "Куки 'token' отсутствует в ответе"
    resp = unauth_api.create_favorite(payload=DEFAULT_PAYLOAD)
    assert resp.status_code == 200, f"{resp.status_code} {resp.text}"
    assert resp.json()["title"] == DEFAULT_PAYLOAD["title"]
    assert resp.json()["lat"] == float(DEFAULT_PAYLOAD["lat"])
    assert resp.json()["lon"] == float(DEFAULT_PAYLOAD["lon"])


@allure.feature("POST /auth/tokens")
@allure.story("Проверка отсутствия токена аутентификации")
@allure.tag("negative")
def test_create_favorite_without_token(unauth_api):
    payload = DEFAULT_PAYLOAD
    resp = unauth_api.create_favorite(payload=payload)
    assert resp.status_code == 401, f"{resp.status_code} {resp.text}"
    assert resp.json()["error"]["message"] == (
        "Параметр 'token' является обязательным"
    )


@allure.feature("POST /v1/auth/tokens")
@allure.story("Проверка использования устаревшего токена аутентификации")
@allure.tag("negative")
def test_create_favorite_with_old_token(unauth_api):
    unauth_api.session.cookies.set(
        "token",
        OLD_TOKEN,
        domain="regions-test.2gis.com",
        path="/",
    )
    payload = DEFAULT_PAYLOAD
    resp = unauth_api.create_favorite(payload=payload)
    assert resp.status_code == 401, f"{resp.status_code} {resp.text}"
    assert resp.json()["error"]["message"] == (
        "Передан несуществующий или «протухший» 'token'"
    )
