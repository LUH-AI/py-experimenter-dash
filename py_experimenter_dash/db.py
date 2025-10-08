from pandas import DataFrame

from py_experimenter_dash.utils.py_experimenter_utils import get_py_experimenter

created = 90


def get_experiment_counts():
    # Mock function
    """Return counts of experiments by status."""
    global created
    if created > 0:
        created = created - 1
    return {
        "total": 100,
        "created": created,
        "running": 1,
        "done": 4 + (100 - created - 9),
        "error": 5,
    }


global py_experimenter
py_experimenter = get_py_experimenter(None, None)

py_experimenter.execute_custom_query("SELECT status, COUNT(*) FROM ml_comparison GROUP BY status")


def get_table() -> DataFrame:
    return py_experimenter.get_table()
