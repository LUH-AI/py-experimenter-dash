from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.db import get_experiment_counts

app = FastAPI()

# --- Setup ---
templates = Jinja2Templates(directory="py_experimenter_dash/templates")
app.mount("/static", StaticFiles(directory="py_experimenter_dash/static"), name="static")

# --- Routes ---


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    counts = get_experiment_counts()
    return templates.TemplateResponse("dashboard.html", {"request": request, "counts": counts})


@app.get("/counts", response_class=HTMLResponse)
async def counts_fragment(request: Request):
    """HTMX endpoint that returns only the updated counts."""
    counts = get_experiment_counts()
    return templates.TemplateResponse("partials/counts.html", {"request": request, "counts": counts})
