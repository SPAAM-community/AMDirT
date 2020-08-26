import pandas as pd
import json
from jsonschema import Draft7Validator
from io import StringIO
from ancientMetagenomeDirCheck.exceptions import DatasetValidationError, DuplicateError
import sys
from rich import print
from rich.console import Console
from rich.table import Table


def check_validity(dataset, schema):
    dt = pd.read_csv(dataset, sep="\t")
    dt_json = json.load((StringIO(dt.to_json(orient="records"))))

    with open(schema, "r") as j:
        json_schema = json.load(j)

    v = Draft7Validator(json_schema)
    errors = []
    for error in sorted(v.iter_errors(dt_json), key=str):
        errors.append(error)
    if len(errors) > 0:
        table = Table(title="Validation Errors were found")
        table.add_column("Offending value", justify="right", style="red", no_wrap=True)
        table.add_column("Line number", style="red")
        table.add_column("Column", justify="right", style="cyan")
        table.add_column("Error", style="magenta")
        lines = []
        for error in errors:
            err_column = list(error.path)[-1]
            err_line = ", ".join(
                [str(i + 2) for i in dt[dt[err_column] == error.instance].index.values]
            )
            lines.append(
                [str(error.instance), err_line, str(err_column), error.message]
            )

        # remove duplicate lines
        b_set = set(tuple(x) for x in lines)
        b = [list(x) for x in b_set]

        for l in b:
            table.add_row(*l)
        console = Console()
        console.print(table)

        raise (DatasetValidationError("DatasetValidationError"))


def check_duplicates(dataset):
    dt = pd.read_csv(dataset, sep="\t")
    if dt.duplicated().sum() != 0:
        message = f"Duplication Error\n{dt[dt.duplicated()]} line is duplicated"
        raise (DuplicateError(message))


def run_tests(dataset, schema):
    try:
        check_duplicates(dataset)
        check_validity(dataset, schema)
        print("[green]All is good, no errors were found ![/green]")
    except (DatasetValidationError, DuplicateError) as e:
        print(f"[red]{e}[/red]")
        sys.exit(1)
