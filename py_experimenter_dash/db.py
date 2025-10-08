from pandas import DataFrame

from py_experimenter_dash.utils.py_experimenter_utils import get_py_experimenter

global py_experimenter
py_experimenter = get_py_experimenter(None, None)


def get_experiment_counts():
    # Mock function
    """Return counts of experiments by status."""
    return py_experimenter.execute_custom_query("SELECT status, COUNT(*) FROM ml_comparison GROUP BY status")


def get_table() -> DataFrame:
    return py_experimenter.get_table()
