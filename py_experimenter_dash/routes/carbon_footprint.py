from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.utils.queries import get_codecarbon_data

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/carbonstats", response_class=JSONResponse)
async def carbonstats(request: Request):
    """Render query form."""
    # values = get_codecarbon_data()
    ccdata = get_codecarbon_data()
    return {"values": ccdata.to_dict()}


@router.get("/carbonstatspart", response_class=HTMLResponse)
async def carbonstats_partial(request: Request):
    """Render query form."""
    ccdata = get_codecarbon_data()
    return templates.TemplateResponse("partials/carbonstats.html", {"request": request, "data": ccdata.to_dict()})


@router.get("/carbonfootprint", response_class=HTMLResponse)
async def get_carbon_footprint(request: Request):
    """Return carbon footprint statistics."""
    ccdata = get_codecarbon_data()
    return templates.TemplateResponse(
        "carbonfootprint.html", {"request": request, "data": ccdata.to_dict(), "active_page": "carbonfootprint"}
    )
