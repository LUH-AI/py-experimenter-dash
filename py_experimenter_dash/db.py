from pandas import DataFrame
from py_experimenter.experimenter import PyExperimenter

pyexp = PyExperimenter(
    experiment_configuration_file_path="tests/experiment_config.yml",
    database_credential_file_path="tests/database_connection.yml",
)


def get_experiment_counts():
    # Mock function
    """Return counts of experiments by status."""
    return {
        "total": 100,
        "open": 90,
        "running": 1,
        "done": 4,
        "error": 5,
    }


def get_table() -> DataFrame:
    return pyexp.get_table()
