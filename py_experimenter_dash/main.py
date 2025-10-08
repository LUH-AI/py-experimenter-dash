# py_experimenter_dash/main.py
import argparse
import os

import uvicorn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_configuration_file_path", required=True)
    parser.add_argument("--database_credentials_file_path", required=True)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    # Pass the arguments via environment variables (used by asgi.py)
    os.environ["EXPERIMENT_CONFIG_FILE_PATH"] = args.experiment_configuration_file_path
    os.environ["DB_CREDENTIALS_FILE_PATH"] = args.database_credentials_file_path

    # Run using import string so reload works properly
    uvicorn.run("py_experimenter_dash.asgi:app", host="127.0.0.1", port=args.port, reload=True)


if __name__ == "__main__":
    main()
