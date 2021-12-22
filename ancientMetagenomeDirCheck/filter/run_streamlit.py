import sys
from streamlit import cli as stcli
from pathlib import Path
import pkg_resources

def get_json_path():
    path = pkg_resources.resource_filename(__name__, "tables.json")
    return path


def run_app(config=None):
    directory = Path(__file__).parent.resolve()
    app = "streamlit.py"
    if config is None:
        config_path = get_json_path()
    else:
        config_path = config
    app_path = f"{directory}/{app}"
    sys.argv = ["streamlit", "run", app_path, "--", "--config", config_path]

    print("\nINFO: To close app, press on your keyboard: ctrl + c")

    sys.exit(stcli.main())

