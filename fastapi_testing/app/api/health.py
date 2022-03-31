from fastapi import APIRouter
from fastapi.requests import Request

router = APIRouter()

@router.get("/")
def get_health(request: Request):
    """

    :param request:
    :return: The base health of the service
    """
    return {"health": "ok"}