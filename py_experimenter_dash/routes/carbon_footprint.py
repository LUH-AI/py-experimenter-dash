from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/carbonstats", response_class=JSONResponse)
async def carbonstats(request: Request):
    """Render query form."""
    # values = get_codecarbon_data()
    values = ""
    labels = ""
    return {"labels": labels, "values": values}


@router.get("/carbonfootprint", response_class=HTMLResponse)
async def get_carbon_footprint(request: Request):
    """Return carbon footprint statistics."""
    return templates.TemplateResponse("carbonfootprint.html", {"request": request, "active_page": "carbonfootprint"})
