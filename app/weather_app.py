from typing import Optional

import fastapi
from fastapi import Depends

from models.location import Location
from models.validation_error import ValidationError
from services import open_weather_service

router = fastapi.APIRouter()


@router.get('/app/weather/{city}')
async def weather(loc: Location = Depends(), units: Optional[str] = 'metric'):
    try:
        res = await open_weather_service.get_report_async(loc.city, loc.state, loc.country, units)
        return res
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)

