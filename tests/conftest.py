from typing import Generator
import pytest
import requests

from config import DEFAULT_HEADERS, BASE_URL
from client.favorites_client import FavoritesClient


@pytest.fixture(scope="session")
def session() -> Generator[requests.Session, None, None]:
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    yield session
    session.close()


@pytest.fixture(scope="function")
def api(session) -> FavoritesClient:
    client = FavoritesClient(base_url=BASE_URL, session=session)
    client.get_token()
    return client


@pytest.fixture(scope="function")
def unauth_api() -> Generator[FavoritesClient, None, None]:
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    client = FavoritesClient(base_url=BASE_URL, session=session)
    try:
        yield client
    finally:
        session.close()
