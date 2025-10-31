![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.4.1-0A9EDC?logo=pytest&logoColor=white)
![Allure](https://img.shields.io/badge/Allure%20Report-2.15.0-ED8B00?logo=allure&logoColor=white)

## Автотесты для сервиса хранения избранных мест:

Сервис предоставляет REST API, и имеет 2 метода:
- POST /v1/favorites
- POST /v1/auth/tokens

Для получения сессионного токена необходимо отправить пустой POST запрос /v1/auth/tokens с пустым телом, и передать его в cookie header запроса POST /v1/favorites, для аутнетификации в виде "token='f3a7d0ba35e94caeabf22554dfdb2e3e'", где 'f3a7d0ba35e94caeabf22554dfdb2e3e' - сессионный токен.

Тело запроса POST /v1/favorites имеет следующее поля: 
- title: Название места. Может содержать латинские и
кириллические символы, цифры и знаки
препинания. Минимальная длина — 1 символ.
Максимальная длина — 999 символов
- lat: Широта (latitude) места
- lon: Долгота (longitude) места
- color (необязательный): Цвет иконки места. Может принимать значения:
BLUE, GREEN, RED, YELLOW

## Примеры запроса и ответа:

- POST /v1/favorites
Запрос:
```
curl -X POST -s https://regions-test.2gis.com/v1/favorites \
-d "title=Париж&lat=48.8575&lon=2.3514&color=RED" \
-b "token=f3a7d0ba35e94caeabf22554dfdb2e3e
```
Ответ:
```
{
    "id": 1761772865871,
    "title": "Париж",
    "lat": 48.8575,
    "lon": 2.3514,
    "color": "RED",
    "created_at": "2025-10-29T22:21:05+00:00"
}
```


