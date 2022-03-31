from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
from .api import api
from fastapi_testing.db.base import database
from .utils import setup_db

app = FastAPI(
    title="A test project",
    description="A project do demonstrate testing with fastapi",
    openapi_url="/services/openapi.json",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(api.api_router, prefix="/services")



@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    The db_session_middleware is a middleware function. Middleware functions are called for each
    request. In this case, when a request is made to the service, a connection is requested against the database.

    That connection becomes a member of the request object. Any database operations that happen during the context of
    the request will run against that connection.
    """

    request.state.db = database
    response: Response = await call_next(request)
    return response


@app.on_event("startup")
async def startup():
    """
        startup() is an event function that fires when the service first starts. Any initialization the service needs to do
        happens here.

        Currently, the only setup taking place is to establish the database session used to handle database requests.
    """

    await database.connect()
    app.database = database
    await setup_db(db=database)


@app.on_event("shutdown")
async def shutdown():
    """
        shutdown() is an event function that fires when the service is shutting down. It's used to perform any
        cleanup operations necessary before the service shuts down.

        Currently, the only cleanup required is removing the database session session.
    """
    await database.disconnect()