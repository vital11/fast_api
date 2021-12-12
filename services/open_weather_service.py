from typing import Optional, Tuple
import httpx

from models.validation_error import ValidationError

api_key: Optional[str] = None


async def get_report_async(city: str, state: Optional[str], country: str, units: str) -> dict:
    city, state, country, units = validate_units(city, state, country, units)

    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'

    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}"

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        if res.status_code != 200:
            raise ValidationError(res.text, status_code=res.status_code)

    data = res.json()
    forecast = data['main']
    return forecast


def validate_units(city: str, state: Optional[str], country: Optional[str], units: str) -> \
        Tuple[str, Optional[str], str, str]:
    city = city.lower().strip()

    if not country:
        country = 'us'
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f'Invalid country {country.upper()}. It must be two letter abbreviation such as US or GB.'
        raise ValidationError(status_code=400, error_msg=error)

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f'Invalid state {state.upper()}. It must be two letter abbreviation such as WA or AK.'
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units = units.strip().lower()

    valid_units = {'standard', 'metric', 'imperial'}
    if units not in valid_units:
        error = f'Invalid units {units}. It must be one of {valid_units}.'
        raise ValidationError(status_code=400, error_msg=error)

    return city, state, country, units

