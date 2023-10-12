from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from webapps.base import api_router as web_api_router


def include_router(app):
    app.include_router(api_router)
    app.include_router(web_api_router)


def configure_static(app):
    """Storing static, html, css, js and media files in these directories"""

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/templates", StaticFiles(directory="templates"), name="templates")
    app.mount("/media/", StaticFiles(directory="media/"), name="media")


def create_tables():
    print("create_tables")
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()
