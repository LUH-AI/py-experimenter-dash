from utils.py_experimenter_utils import get_py_experimenter


def test_get_py_experimenter():
    database_name = "pyexp_dash"
    table_name = "ml_comparison"
    experimenter = get_py_experimenter(database_name, table_name)
    assert experimenter is not None
