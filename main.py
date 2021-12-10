import json
from pathlib import Path

from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles

from app import weather_app
from services import open_weather_service
from views import home

app = FastAPI()


def configure():
    configure_routing()
    configure_app_keys()


def configure_routing():
    app.mount('/static', StaticFiles(directory='static'), name='static')
    app.include_router(home.router)
    app.include_router(weather_app.router)


def configure_app_keys():
    file = Path('settings.json').absolute()
    if not file.exists():
        print(f"WARNING: {file} file not found, you cannot continue, please see settings_template.json")
        raise Exception("settings.json file not found, you cannot continue, please see settings_template.json")

    with open('settings.json') as f:
        settings = json.load(f)
        open_weather_service.api_key = settings.get('api_key')


if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=8000, host='127.0.0.1')
else:
    configure()




