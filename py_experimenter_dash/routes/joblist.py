from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/joblist", response_class=HTMLResponse)
async def errors_page(request: Request):
    """Show a summary of errored experiments (e.g., last 20)."""

    return templates.TemplateResponse("jobs.html", {"request": request, "active_page": "joblist"})
