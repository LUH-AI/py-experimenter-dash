# ruff: noqa: S608
import os
from typing import Optional

from pandas import DataFrame
from py_experimenter.experimenter import PyExperimenter


def get_py_experimenter(database_name: Optional[str], table_name: Optional[str]) -> PyExperimenter:
    return PyExperimenter(
        experiment_configuration_file_path=os.getenv("EXPERIMENT_CONFIG_FILE_PATH"),
        database_credential_file_path=os.getenv("DB_CREDENTIALS_FILE_PATH"),
        database_name=database_name,
        table_name=table_name,
        use_codecarbon=False,
    )


def get_experiment_status_overview(database_name: str, table_name: str) -> DataFrame:
    experimenter = get_py_experimenter(database_name, table_name)
    result = experimenter.execute_custom_query(f"SELECT status, COUNT(*) as count FROM {table_name} GROUP BY status")
    return result
