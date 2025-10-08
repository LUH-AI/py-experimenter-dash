from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()

carbon = 5


@router.get("/carbonstats", response_class=JSONResponse)
async def carbonstats(request: Request):
    """Render query form."""
    global carbon
    carbon += 5
    labels = ["Carbon", "Static"]
    values = [carbon, 5]

    return {"labels": labels, "values": values}


@router.get("/carbonfootprint", response_class=HTMLResponse)
async def get_carbon_footprint(request: Request):
    """Return carbon footprint statistics."""
    return templates.TemplateResponse("carbonfootprint.html", {"request": request, "active_page": "carbonfootprint"})
