import sys
from streamlit import cli as stcli
from pathlib import Path


def run_app(config=None):
    directory = Path(__file__).parent.resolve()
    app = "streamlit.py"
    if config is None:
        config_path = f"{directory}/tables.json"
    else:
        config_path = config
    app_path = f"{directory}/{app}"

    sys.argv = ["streamlit", "run", app_path, "--", "--config", config_path]
    sys.exit(stcli.main())
