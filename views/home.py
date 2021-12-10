import fastapi
from starlette.requests import Request

from starlette.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates('templates')


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('home/index.html', context={'request': request})

