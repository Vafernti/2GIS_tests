from datetime import datetime, timedelta, timezone
import allure
import pytest

from constants import (
    DEFAULT_LATITUDE,
    DEFAULT_LONGITUDE,
    DEFAULT_TITLE,
    DEFAULT_PAYLOAD,
    LAT_LEVELS,
    LON_LEVELS
)

PAIRS = [(lat, lon) for lat in LAT_LEVELS for lon in LON_LEVELS]


@allure.feature("POST /v1/favorites")
@allure.story("Проверка успешного создания избранного места")
@allure.tag("positive", "smoke")
def test_create_favorite_default_payload(api):
    resp = api.create_favorite(payload=DEFAULT_PAYLOAD)
    assert resp.status_code == 200, f"{resp.status_code} {resp.json()}"
    assert resp.json()["title"] == DEFAULT_TITLE
    assert resp.json()["lat"] == float(DEFAULT_LATITUDE)
    assert resp.json()["lon"] == float(DEFAULT_LONGITUDE)


@allure.feature("POST /v1/favorites")
@allure.story("Создание избранного места, валидация поля title")
@allure.tag("positive", )
@pytest.mark.parametrize(
    "title",
    [
        "дом",
        "home",
        "Cafe 123",
        "Ул. Арбат",
        "Arbat St.",
        "1234567890",
        "'.,:;!?-—()[]{}'\"«»/@&%#№'",
        "x" * 1,
        "x" * 999,
    ],
    ids=[
        "russian_word",
        "english_word",
        "latin_and_digits",
        "russian_with_special",
        "english_with_special",
        "digits_only",
        "special_characters",
        "length_10",
        "length_999 (max allowed)",
    ],
)
def test_create_favorite_success(api, title):
    payload = {
        "title": title,
        "lat": DEFAULT_LATITUDE,
        "lon": DEFAULT_LONGITUDE,
    }
    resp = api.create_favorite(payload=payload)
    assert resp.status_code == 200, f"{resp.status_code} {resp.json()}"
    assert resp.json()["title"] == title


@allure.feature("POST /v1/favorites")
@allure.story("Создание избранного места, валдиация поля title")
@allure.tag("negative")
@pytest.mark.parametrize(
    "title",
    [
        None,
        "",
        " ",
        "x" * 1000,
        1234,
    ],
    ids=[
        "null_field",
        "empty_field",
        "space_only",
        "length_1000 (exceeds max)",
        "int_type",
    ],
)
def test_create_favorite_negative(api, title):
    payload = {
        "title": title,
        "lat": DEFAULT_LATITUDE,
        "lon": DEFAULT_LONGITUDE,
    }
    resp = api.create_favorite(payload=payload)
    assert resp.status_code == 400, f"{resp.status_code} {resp.json()}"


@allure.feature("POST /v1/favorites")
@allure.story("Создание избранного места — валидация поля lat")
@allure.tag("positive")
@pytest.mark.parametrize(
    "lat",
    [
        0,
        45,
        -45,
        -90.0,
        90.0,
        48.8575,
        -48.8575,

    ],
    ids=[
        "zero_latitude",
        "positive_latitude",
        "negative_latitude",
        "lat=-90 (min_boundary)",
        "lat=90 (max_boundary)",
        "float_latitude",
        "negative_float_latitude",
    ],
)
def test_create_favorite_lat_positive(api, lat):
    payload = {
        "title": DEFAULT_TITLE,
        "lat": lat,
        "lon": DEFAULT_LONGITUDE,
    }
    resp = api.create_favorite(payload=payload)
    assert resp.status_code == 200, f"{resp.status_code} {resp.json()}"
    assert resp.json()["lat"] == lat


@allure.feature("POST /v1/favorites")
@allure.story("Создание избранного места — валидация поля lat")
@allure.tag("negative")
@pytest.mark.parametrize(
    "lat",
    [
        None,
        "",
        "'48.8575'",
        "Париж",
        True,
        -90.0001,
        90.0001,
        999999,
    ],
    ids=[
        "null_field",
        "empty_string",
        "string_number",
        "text",
        "bool_type",
        "below_min",
        "above_max",
        "too_large_number",
    ],
)
def test_create_favorite_lat_negative(api, lat):
    payload = {
        "title": DEFAULT_TITLE,
        "lat": lat,
        "lon": DEFAULT_LONGITUDE,
    }
    resp = api.create_favorite(payload=payload)
    assert resp.status_code == 400, f"{resp.status_code} {resp.json()}"


@allure.feature("POST /v1/favorites")
@allure.story("Создание избранного места — валидация поля lon")
@allure.tag("positive")
@pytest.mark.parametrize(
    "lon",
    [
        0,
        45,
        -45,
        -180.0,
        180.0,
        48.8575,
        -48.8575,

    ],
    ids=[
        "zero_latitude",
        "positive_latitude",
        "negative_latitude",
        "lat=-180 (min_boundary)",
        "lat=180 (max_boundary)",
        "float_latitude",
        "negative_float_latitude",
    ],
)
def test_create_favorite_lon_positive(api, lon):
    payload = {
        "title": DEFAULT_TITLE,
        "lat": DEFAULT_LATITUDE,
        "lon": lon,
    }
    resp = api.create_favorite(payload=payload)
    assert resp.status_code == 200, f"{resp.status_code} {resp.json()}"
    assert resp.json()["lon"] == lon


@allure.feature("POST /v1/favorites")
@allure.story("Создание избранного места — валидация поля lon")
@allure.tag("negative")
@pytest.mark.parametrize(
    "lon",
    [
        None,
        "",
        "'2.3514'",
        "Париж",
        True,
        -180.0001,
        180.0001,
        999999,
    ],
    ids=[
        "null_field",
        "empty_string",
        "string_number",
        "text",
        "bool_type",
        "below_min",
        "above_max",
        "too_large_number",
    ],
)
def test_create_favorite_lon_negative(api, lon):
    payload = {
        "title": DEFAULT_TITLE,
        "lat": DEFAULT_LATITUDE,
        "lon": lon,
    }
    resp = api.create_favorite(payload=payload)
    assert resp.status_code == 400, f"{resp.status_code} {resp.json()}"


@allure.feature("POST /v1/favorites")
@allure.story("Pairwise: lat×lon (минимальный 3×3)")
@allure.tag("positive")
@pytest.mark.parametrize(
    "lat,lon",
    PAIRS,
    ids=[f"lat={lat};lon={lon}" for lat, lon in PAIRS],
)
def test_pairwise_lat_lon(api, lat, lon):
    payload = {"title": DEFAULT_TITLE, "lat": lat, "lon": lon}
    resp = api.create_favorite(payload=payload)
    assert resp.status_code == 200, f"{resp.status_code} {resp.text}"
    data = resp.json()
    assert data["lat"] == lat
    assert data["lon"] == lon


@allure.feature("POST /v1/favorites")
@allure.story(
    "Создание избранного места — валидация поля color (позитивные значения)"
)
@allure.tag("positive")
@pytest.mark.parametrize(
    "color",
    [
        "BLUE",
        "RED",
        "GREEN",
        "YELLOW"
    ],
    ids=[
        "none_value",
        "valid_blue",
        "valid_red",
        "valid_green",
    ],
)
def test_create_favorite_color_positive(api, color):
    payload = {
        "title": DEFAULT_TITLE,
        "lat": DEFAULT_LATITUDE,
        "lon": DEFAULT_LONGITUDE,
        "color": color,
    }

    resp = api.create_favorite(payload)
    assert resp.status_code == 200, f"{resp.status_code} {resp.text}"
    assert resp.json()["color"] == color


@allure.feature("POST /v1/favorites")
@allure.story(
    "Создание избранного места — валидация поля color (негативные значения)"
)
@allure.tag("negative")
@pytest.mark.parametrize(
    "color",
    [
        "blue",
        "BlUe",
        "WHITE",
        "",
        " ",
        "@!#?",
        "123",
        123,
        " BlUE",
        "GREEN ",
        "A" * 256,
    ],
    ids=[
        "lowercase_word",
        "mixed_case_word",
        "invalid_color",
        "empty_string",
        "space_only",
        "special_symbols",
        "digits_str",
        "int",
        "leading_space",
        "trailing_space",
        "long_string",
    ],
)
def test_create_favorite_color_negative(api, color):
    payload = {
        "title": DEFAULT_TITLE,
        "lat": DEFAULT_LATITUDE,
        "lon": DEFAULT_LONGITUDE,
        "color": color,
    }
    resp = api.create_favorite(payload)
    assert resp.status_code == 400, f"{resp.status_code} {resp.text}"


@allure.feature("POST /v1/favorites")
@allure.story("Проверка created_at — корректная дата создания")
@allure.tag("positive")
def test_created_at_timestamp(api):
    before = datetime.now(timezone.utc)
    resp = api.create_favorite(payload=DEFAULT_PAYLOAD)
    assert resp.status_code == 200, f"{resp.status_code} {resp.text}"
    after = datetime.now(timezone.utc)
    data = resp.json()
    created_at_str = data.get("created_at")
    assert created_at_str, "Поле created_at отсутствует или пустое"
    created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
    assert before <= created_at <= after + timedelta(seconds=2), (
        f"created_at вне диапазона: {created_at_str}, "
        f"ожидалось между {before} и {after}"
    )
