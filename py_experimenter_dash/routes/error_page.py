from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/errors", response_class=HTMLResponse)
async def errors_page(request: Request):
    """Show a summary of errored experiments (e.g., last 20)."""
    result = [{"error": "Stacktrace: ValueError", "count": 432}]
    return templates.TemplateResponse("errors.html", {"request": request, "errors": result, "active_page": "errors"})
