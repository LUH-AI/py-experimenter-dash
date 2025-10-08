# ruff: noqa: S608
import pandas as pd

from py_experimenter_dash.utils.py_experimenter_utils import get_py_experimenter

global py_experimenter
py_experimenter = get_py_experimenter(None, None)


def get_table() -> pd.DataFrame:
    return py_experimenter.get_table()


def get_table_snapshot(table_name: str, limit: int) -> pd.DataFrame:
    return py_experimenter.execute_custom_query(f"SELECT * FROM {table_name} LIMIT {limit};")


def get_status_overview() -> pd.DataFrame:
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


def get_errors() -> pd.DataFrame:
    table_name = py_experimenter.config.database_configuration.table_name
    query = (
        f"SELECT DISTINCT(error), COUNT(*) as error_count FROM {table_name} GROUP BY error ORDER BY error_count DESC;"
    )

    return py_experimenter.execute_custom_query(query)


def create_history_query() -> None:
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


def get_codecarbon_data() -> pd.DataFrame:
    table_name = py_experimenter.config.database_configuration.table_name
    codecarbon_table = f"{table_name}__codecarbon"
    query = f"""
    SELECT
        SUM(cpu_energy_kw) AS cpu_energy_kw,
        SUM(gpu_energy_kw) AS gpu_energy_kw,
        SUM(ram_energy_kw) AS ram_energy_kw,
        SUM(emissions_kg) AS emissions_kg,
        SUM(duration_seconds) AS duration_seconds,
        SUM(energy_consumed_kw) AS energy_consumed_kw
    FROM {codecarbon_table}
    LIMIT 100
    """
    return py_experimenter.execute_custom_query(query)


def get_table_structure() -> pd.DataFrame:
    if py_experimenter.config.database_configuration.provider != "mysql":
        raise NotImplementedError("get_table_structure is only implemented for MySQL databases.")
    table_name = py_experimenter.config.database_configuration.table_name
    # Get all tables that start with the table name
    query = f"""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = DATABASE()
    AND table_name LIKE '{table_name}%';
    """

    tables = py_experimenter.execute_custom_query(query)

    # For each table, get the columns and their types
    table_structure = {}
    for _, row in tables.iterrows():
        table = row["table_name"]
        table_structure[table] = {}
        query = f"DESCRIBE {table};"
        columns = py_experimenter.execute_custom_query(query)
        col_types = {}
        for _, col in columns.iterrows():
            col_types[col["Field"]] = col["Type"]
        table_structure[table] = col_types

    return table_structure


def add_query_to_history(query: str) -> None:
    # Check if the query already exists in the history table
    query_check = f"SELECT id, query_count FROM query_history WHERE query = {query};"
    result = py_experimenter.execute_custom_query(query_check)
    if result.empty:
        # If the query does not exist, insert it
        query_upsert = f"""
            INSERT INTO query_history (query)
            VALUES ({query})
            ON CONFLICT(query) DO UPDATE SET
                query_count = query_history.query_count + 1,
                last_timestamp = CURRENT_TIMESTAMP;
        """
    else:
        # If the query exists, update the count and timestamp
        query_upsert = f"""
            UPDATE query_history
            SET query_count = query_count + 1,
                last_timestamp = CURRENT_TIMESTAMP
            WHERE query = {query};
        """
    py_experimenter.execute_custom_query(query_upsert)


def get_query_history() -> pd.DataFrame:
    query = """
        SELECT query, query_count, first_timestamp, last_timestamp
        FROM query_history
        ORDER BY last_timestamp DESC;
    """
    return py_experimenter.execute_custom_query(query)
