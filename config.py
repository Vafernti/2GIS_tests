import os

BASE_URL = os.getenv("BASE_URL", "https://regions-test.2gis.com")

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}
