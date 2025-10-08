from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.utils.queries import get_table

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/joblist", response_class=HTMLResponse)
async def errors_page(request: Request):
    """Show a summary of errored experiments (e.g., last 20)."""

    return templates.TemplateResponse("jobs.html", {"request": request, "active_page": "joblist"})


@router.get("/jobs", response_class=HTMLResponse)
async def get_jobs(request: Request):
    """
    Returns the table as a json.
    """

    table = get_table()
    table = table.fillna("").to_dict()
    table_keys = table.keys()
    table_len = len(table[next(iter(table_keys))])
    table = [{k: table[k][i] for k in table_keys} for i in range(table_len)]

    return templates.TemplateResponse(
        "partials/jobstable.html", {"request": request, "table": table, "keys": table_keys}
    )
