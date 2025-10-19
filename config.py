import yaml
from pathlib import Path

config_path = Path(__file__).parent / "config.yml"

with open(config_path, "r") as f:
    cfg = yaml.safe_load(f)

DATABASE_URL = cfg["database"]["url"]
