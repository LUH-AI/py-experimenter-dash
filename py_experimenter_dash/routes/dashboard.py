from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.db import get_experiment_counts

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    counts = get_experiment_counts()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "counts": counts, "active_page": "dashboard"}
    )


@router.get("/counts", response_class=HTMLResponse)
async def counts_fragment(request: Request):
    """HTMX endpoint that returns only the updated counts."""
    counts = get_experiment_counts()
    return templates.TemplateResponse("partials/counts.html", {"request": request, "counts": counts})
