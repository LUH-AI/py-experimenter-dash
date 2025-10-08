from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from py_experimenter_dash.db import get_experiment_counts

app = FastAPI()

# --- Setup ---
templates = Jinja2Templates(directory="py_experimenter_dash/templates")
app.mount("/static", StaticFiles(directory="py_experimenter_dash/static"), name="static")

carbon = 5

# --- Routes ---


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    counts = get_experiment_counts()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "counts": counts, "active_page": "dashboard"}
    )


@app.get("/errors", response_class=HTMLResponse)
async def errors_page(request: Request):
    """Show a summary of errored experiments (e.g., last 20)."""
    result = [{"error": "Stacktrace: ValueError", "count": 432}]
    return templates.TemplateResponse("errors.html", {"request": request, "errors": result, "active_page": "errors"})


@app.get("/carbonstats", response_class=JSONResponse)
async def carbonstats(request: Request):
    """Render query form."""
    global carbon
    carbon += 5
    labels = ["Carbon", "Static"]
    values = [carbon, 5]

    return {"labels": labels, "values": values}


@app.get("/carbonfootprint", response_class=HTMLResponse)
async def carbon_footprint(request: Request):
    """Return carbon footprint statistics."""
    return templates.TemplateResponse("carbonfootprint.html", {"request": request, "active_page": "carbonfootprint"})


@app.get("/query", response_class=HTMLResponse)
async def query_page(request: Request):
    """Render query form."""
    return templates.TemplateResponse(
        "query.html", {"request": request, "rows": None, "query": "", "error": None, "active_page": "query"}
    )


@app.post("/query", response_class=HTMLResponse)
async def run_query(request: Request, sql_query: str = Form(...)):
    """Execute arbitrary SQL query on the experiments database."""
    error = "None"
    table = "<table><tr><td>Test</td></tr></table>"
    return templates.TemplateResponse(
        "query.html",
        {"request": request, "table": table, "query": sql_query, "error": error, "active_page": "query"},
    )


@app.get("/counts", response_class=HTMLResponse)
async def counts_fragment(request: Request):
    """HTMX endpoint that returns only the updated counts."""
    counts = get_experiment_counts()
    return templates.TemplateResponse("partials/counts.html", {"request": request, "counts": counts})
