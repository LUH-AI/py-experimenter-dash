from py_experimenter.experimenter import PyExperimenter


def get_py_experimenter(database_name: str, table_name: str) -> PyExperimenter:
    return PyExperimenter(
        experiment_configuration_file_path="config/mock_expdriment.yml",
        database_credential_file_path="config/database_credentials.yml",
        database_name=database_name,
        table_name=table_name,
        use_codecarbon=False,
    )
