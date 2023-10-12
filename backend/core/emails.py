import random

from fastapi import APIRouter
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig
from fastapi_mail import FastMail
from fastapi_mail import MessageSchema
from fastapi_mail import MessageType


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# in this case, an instance of the Connection Config class is used to establish a connection
conf = ConnectionConfig(
    MAIL_USERNAME="grymes44@gmail.com",
    MAIL_PASSWORD="wcweueiveizpjpiu",
    MAIL_FROM="grymes44@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


# Link to go to the website with a successful registration form
url = "http://localhost:8000/?msg=Successfully-Registered"


@router.post("/confirm-email")
async def verify_email(email: str):
    """This function responsible for send message"""

    # This html forms a mail email confirmation button
    html = f"""
    <a href={url}>
      <input type="submit" value="Confirm" style=
      "color: white;
       background: #0067d4;
       font-size: 0.9em;
       border: none;
       outline: none;
       padding: 9px 25px;
       cursor: pointer;">
    </a>
    """

    # This instance of the Message Schema class is responsible for the configuration of the message schema
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body=f"Thank you for registering! Please click the following link to confirm your email:"
        f"{html}",
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
