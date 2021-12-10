from pprint import pprint
from typing import Optional
import requests


api_key: Optional[str] = None


def get_report(city: str, state: Optional[str], country: str, units: str) -> dict:
    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'

    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}"
    print(url)

    res = requests.get(url)
    res.raise_for_status()

    data = res.json()
    forecast = data['main']
    pprint(forecast)
    return forecast




