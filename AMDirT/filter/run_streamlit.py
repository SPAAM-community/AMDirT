import logging
import sys
from streamlit import cli as stcli
from pathlib import Path
from AMDirT.filter.utils import get_json_path

def run_app(tables=None):
    directory = Path(__file__).parent.resolve()
    app = "streamlit.py"
    if tables is None:
        config_path = get_json_path()
    else:
        config_path = config
    app_path = f"{directory}/{app}"

    sys.argv = ["streamlit", "run", app_path, "--", "--config", config_path]
    logging.info("\n[AMDirT] To close app, press on your keyboard: ctrl+c\n")
    sys.exit(stcli.main())
