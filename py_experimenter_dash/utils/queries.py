# ruff: noqa: S608
import pandas as pd
from py_experimenter.experimenter import PyExperimenter


def get_table_snapchot(py_experimenter: PyExperimenter) -> pd.DataFrame:
    return py_experimenter.get_table(condition="")


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
    query = (
        f"SELECT DISTINCT(error), COUNT(*) as error_count FROM {table_name} GROUP BY error ORDER BY error_count DESC;"
    )

    return py_experimenter.execute_custom_query(query)


def create_history_query(py_experimenter: PyExperimenter) -> None:
    # SQLite schema: track first and most recent time we saw a query
    query = """
    CREATE TABLE IF NOT EXISTS query_history (
        id INTEGER PRIMARY KEY,
        query TEXT NOT NULL UNIQUE,
        query_count INTEGER NOT NULL DEFAULT 1,
        first_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_timestamp  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    py_experimenter.execute_custom_query(query)


def add_query_to_history(py_experimenter: PyExperimenter, query: str) -> None:
    """
    Inserts a new query (count=1, timestamps now) or, if it exists,
    increments count and updates last_timestamp.
    """
    query_upsert = """
        INSERT INTO query_history (query)
        VALUES (?)
        ON CONFLICT(query) DO UPDATE SET
            query_count = query_history.query_count + 1,
            last_timestamp = CURRENT_TIMESTAMP;
    """
    py_experimenter.execute_custom_query(query_upsert, (query,))


def get_query_history(py_experimenter: PyExperimenter) -> pd.DataFrame:
    query = """
        SELECT query, query_count, first_timestamp, last_timestamp
        FROM query_history
        ORDER BY last_timestamp DESC;
    """
    return py_experimenter.execute_custom_query(query)
