from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.db import get_experiment_counts

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    counts_df = get_experiment_counts()
    counts = dict(zip(counts_df["status"], counts_df["COUNT(*)"]))
    total = sum(counts.values())
    counts["total"] = total

    status_keys = ["running", "created", "error", "done"]
    for status_key in status_keys:
        if status_key not in counts:
            counts[status_key] = 0
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "counts": counts, "active_page": "dashboard"}
    )


@router.get("/counts", response_class=HTMLResponse)
async def counts_fragment(request: Request):
    """HTMX endpoint that returns only the updated counts."""
    counts_df = get_experiment_counts()
    counts = dict(zip(counts_df["status"], counts_df["COUNT(*)"]))
    total = sum(counts.values())
    counts["total"] = total

    status_keys = ["running", "created", "error", "done"]
    for status_key in status_keys:
        if status_key not in counts:
            counts[status_key] = 0

    return templates.TemplateResponse("partials/counts.html", {"request": request, "counts": counts})
