created = 90


def get_experiment_counts():
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
