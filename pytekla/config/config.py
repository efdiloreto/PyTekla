import os
import sys
import json
from pathlib import Path


CONFIG_FILE_PATH = Path(__file__).with_name("config.json")


def set_tekla_path(path):
    if not os.path.exists(path):
        sys.stderr.write(f"Error: Path {path} does not exist.")
        return

    with CONFIG_FILE_PATH.open("r") as f:
        config = json.load(f)

    config["bin_path"] = path

    with CONFIG_FILE_PATH.open("w") as f:
        json.dump(config, f, indent=4)

    sys.stderr.write(
        "\n\033[92m"
        + f"Successfully updated bin_path to {path} in config.json"
        + "\033[0m"
    )


def _read_tekla_path():
    with CONFIG_FILE_PATH.open("r") as f:
        config = json.load(f)
        return config.get("bin_path", None)
