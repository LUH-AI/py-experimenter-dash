from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.utils.py_experimenter_utils import get_py_experimenter
from py_experimenter_dash.utils.queries import get_errors

global py_experimenter
py_experimenter = get_py_experimenter(None, None)


templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/errors", response_class=HTMLResponse)
async def errors_page(request: Request):
    """Show a summary of errored experiments (e.g., last 20)."""
    errors_df = get_errors(py_experimenter)
    errors = errors_df.to_dict(orient="records")
    res = []
    if len(errors) == 1 and errors[0]["error"] == "None":
        errors = False
    else:
        for error in errors:
            if error["error"] is not None:
                error["error"] = error["error"].replace("\\n", "<br>")
                res.append(error)

    return templates.TemplateResponse("errors.html", {"request": request, "errors": res, "active_page": "errors"})
