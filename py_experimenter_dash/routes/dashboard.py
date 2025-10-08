from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.db import get_experiment_counts, get_table

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


@router.get("/jobs", response_class=JSONResponse)
async def get_jobs(request: Request):
    """
    Returns the table as a json.
    """

    table = get_table()
    table = table.fillna(-1).to_dict()
    table_keys = table.keys()
    table_len = len(table[next(iter(table_keys))])
    table = [{k: table[k][i] for k in table_keys} for i in range(table_len)]

    table = sorted(table, key=lambda x: x["creation_date"], reverse=True)

    return table
