import random
from time import sleep

from py_experimenter.experimenter import PyExperimenter

produce_errors = True


def run_experiment(config, result_processor, custom_config):
    sleep(10 * random.random())
    result_processor.process_results({
        "accuracy": random.random(),
        "traintime": random.randint(1, 5000),
        "testtime": random.randint(1, 100),
        "done": "True",
    })
    random.random()


def run_error_experiment(config, result_processor, custom_config):
    if random.random() > 0.25:
        raise ValueError("foo")
    else:
        raise NotImplementedError()


pyexp = PyExperimenter(
    experiment_configuration_file_path="experiment_config.yml",
    database_credential_file_path="../config/database_credentials.yml",
    use_codecarbon=False,
)
pyexp.fill_table_from_config()
pyexp.execute(run_experiment, max_experiments=10)
pyexp.execute(run_error_experiment, max_experiments=10)
