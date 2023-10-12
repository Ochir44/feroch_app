from pydantic import BaseModel


class Token(BaseModel):
    """These parameters will be used to verify that in the module
    route_login.py/login_for_access_token the same parameters are returned.
    """

    access_token: str
    token_type: str
