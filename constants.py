# Payload constants
DEFAULT_TITLE = "Fav place"
DEFAULT_LATITUDE = "55.7558"
DEFAULT_LONGITUDE = "37.6176"
DEFAULT_PAYLOAD = {
    "title": DEFAULT_TITLE,
    "lat": DEFAULT_LATITUDE,
    "lon": DEFAULT_LONGITUDE,
}

OLD_TOKEN = 'e6b5d508fb4e4f34925035a906ab35da'

LAT_LEVELS = [-90.0, 0.0, 90.0]
LON_LEVELS = [-180.0, 0.0, 180.0]

MISSING_TITLE_ERR = "Параметр 'title' является обзательным"
EMPTY_TITLE_ERR = "Параметр 'title' не может быть пустым"
BOUNDARY_TITLE_ERR = "Параметр 'title' должен содержать не более 999 символов"
