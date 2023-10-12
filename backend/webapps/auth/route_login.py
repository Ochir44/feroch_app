from apis.version1.route_login import login_for_access_token
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from webapps.auth.forms import LoginForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    """Returns an empty login form"""

    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    """This function will provide the user with filling out a login form and
    sending a request for publication, which will contain the data entered by users.
    """

    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            """If the form is valid we are creating a template response which we
            pass in one of our internal functions as it requires a response as a parameter.
            """

            form.__dict__.update(msg="Login Successful")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)

            # The login_for_access_token function checks the correctness of the username and password
            await login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            """In case any HttpException occurs we are assuming
            that the username and password were incorrect and updating form.errors.
            """

            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)
