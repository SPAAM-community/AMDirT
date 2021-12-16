import sys
from streamlit import cli as stcli
from pathlib import Path


def run_app():
    directory = Path(__file__).parent.resolve()
    app = "streamlit.py"
    p = Path(f"{directory}/{app}")
    print(p)
    sys.argv = ["streamlit", "run", str(p)]
    sys.exit(stcli.main())
