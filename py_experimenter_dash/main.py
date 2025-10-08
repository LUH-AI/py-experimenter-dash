from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.routes import carbon_footprint, dashboard, error_page, query

app = FastAPI()


# --- Setup ---
templates = Jinja2Templates(directory="py_experimenter_dash/templates")
app.mount("/static", StaticFiles(directory="py_experimenter_dash/static"), name="static")

app.include_router(dashboard.router)
app.include_router(error_page.router)
app.include_router(query.router)
app.include_router(carbon_footprint.router)
