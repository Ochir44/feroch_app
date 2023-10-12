from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="templates"
)  # Jinja2 will search for html files inside the templates folder
general_pages_router = APIRouter()  # Used to declare a path operation


@general_pages_router.get("/")
async def home(request: Request):
    """This function captures
    the request and returns an HTMResponse
    with the request in the dictionary
    """

    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request}
    )
