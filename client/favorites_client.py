from typing import Dict, Optional, Any
import requests
import allure


class FavoritesClient:

    def __init__(
            self,
            base_url: str,
            session: requests.Session,
            headers: Optional[dict] = None
    ):
        self.session = session
        if headers:
            self.session.headers.update(headers)
        self.base_url = base_url

    @allure.step("POST /v1/auth/tokens")
    def get_token(self) -> requests.Response:
        """Получает токен и добавляет его в сессию для последующих запросов."""
        url = f"{self.base_url}/v1/auth/tokens"
        resp = self.session.post(url)
        token = resp.cookies.get("token")
        self.session.cookies.set(
            "token",
            token,
            domain="regions-test.2gis.com",
            path="/",
        )
        return resp

    @allure.step("POST /v1/favorites")
    def create_favorite(
        self,
        payload: Dict[str, Any]
    ) -> requests.Response:
        url = f"{self.base_url}/v1/favorites"
        resp = self.session.post(url, data=payload)
        return resp
