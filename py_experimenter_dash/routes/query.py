from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.utils.queries import get_table_structure

templates = Jinja2Templates(directory="py_experimenter_dash/templates")
router = APIRouter()


@router.get("/query", response_class=HTMLResponse)
async def query_page(request: Request):
    """Render query form."""
    return templates.TemplateResponse(
        "query.html", {"request": request, "rows": None, "query": "", "error": None, "active_page": "query"}
    )


@router.post("/query", response_class=HTMLResponse)
async def run_query(request: Request, sql_query: str = Form(...)):
    """Execute arbitrary SQL query on the experiments database."""
    error = "None"
    table = "<table><tr><td>Test</td></tr></table>"
    return templates.TemplateResponse(
        "query.html",
        {"request": request, "table": table, "query": sql_query, "error": error, "active_page": "query"},
    )


@router.get("/queries")
async def get_query_history(request: Request) -> list[str]:
    return [
        "select * from table",
        "select field from table",
        "select field from table where field=value",
    ]


@router.get("/tables", response_class=HTMLResponse)
async def get_table_info(request: Request) -> list[dict]:
    tsdf = get_table_structure()
    return templates.TemplateResponse("partials/tablepanel.html", {"request": request, "tables": tsdf})
