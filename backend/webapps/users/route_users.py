import asyncio

import requests
from core.emails import verify_email
from db.models.users import Users
from db.repository.users import create_new_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from webapps.users.forms import UserCreateForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/register/")
def register(request: Request):
    """Returns an empty registration form"""

    return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    """This feature will provide the user with the opportunity to fill out a registration form and
    send a publication request that will contain the data entered by users.
    """

    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            username=form.username.lower(),
            email=form.email,
            password=form.password,
            confirm_password=form.confirm_password,
        )
        if db.query(Users).filter(Users.username == user.username).first():
            # in case of any error, we update form.errors
            form.__dict__.get("errors").append(
                "A user with this name is already registered"
            )
        if db.query(Users).filter(Users.email == user.email).first():
            form.__dict__.get("errors").append(
                "A user with this email is already registered"
            )
        else:
            await verify_email(email=user.email)  # Confirm email
            if await create_new_user(user=user, db=db):
                # Returns form with the confirmation of the mail
                return templates.TemplateResponse(
                    "users/confirm_email.html", form.__dict__
                )

    # Returns registration form
    return templates.TemplateResponse("users/register.html", form.__dict__)


@router.get("/confirm-email")
def confirm_email():
    """Returns the confirm email form"""

    return responses.RedirectResponse(
        "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
    )
