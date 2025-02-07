from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from bookings.router import router_booking
from club.router import router_club
from club.zone.router import router_zone
from club.zone.table.router import router_table
from pages.router import router_frontend
from users.router import router_users, router_auth

app = FastAPI()

app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_booking)
app.include_router(router_club)
app.include_router(router_zone)
app.include_router(router_table)
app.include_router(router_frontend)


app.mount("/static", StaticFiles(directory="static/"), "static")
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
