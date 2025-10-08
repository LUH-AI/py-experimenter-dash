# ruff: noqa: S608
import pandas as pd
from py_experimenter.experimenter import PyExperimenter


def get_status_overview(py_experimenter: PyExperimenter) -> pd.DataFrame:
    table_name = py_experimenter.config.database_configuration.table_name
    query = (
        "SELECT status, COUNT(*) AS count"
        f" FROM {table_name}"
        " GROUP BY status"
        " UNION ALL"
        " SELECT 'Total' AS status, COUNT(*) AS count"
        f" FROM {table_name};"
    )

    return py_experimenter.execute_custom_query(query)


def get_errors(py_experimenter: PyExperimenter) -> pd.DataFrame:
    table_name = py_experimenter.config.database_configuration.table_name
    query = f"SELECT DISTINCT(error) FROM {table_name}"

    return py_experimenter.execute_custom_query(query)
