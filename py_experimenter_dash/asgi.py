import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.routes import carbon_footprint, dashboard, error_page, query

templates = Jinja2Templates(directory="py_experimenter_dash/templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")


experiment_config_file = os.getenv("EXPERIMENT_CONFIG_PATH", "configs/default_experiment.yaml")
database_credentials_file = os.getenv("DB_CREDENTIALS_PATH", "configs/default_db.yaml")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="py_experimenter_dash/static"), name="static")
app.state.experiment_config_file = experiment_config_file
app.state.database_credentials_file = database_credentials_file

# Static and routes
app.mount("/static", StaticFiles(directory="py_experimenter_dash/static"), name="static")
app.include_router(dashboard.router)
app.include_router(error_page.router)
app.include_router(query.router)
app.include_router(carbon_footprint.router)
