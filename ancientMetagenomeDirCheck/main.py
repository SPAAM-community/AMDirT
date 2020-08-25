import pandas as pd
import json
from jsonschema import Draft7Validator
from io import StringIO
from ancientMetagenomeDirCheck.exceptions import DatasetValidationError, DuplicateError
import sys


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
        print("Validation Errors were found")
        for error in errors:
            err_column = list(error.path)[-1]
            print("- ", error.message, f"in column {err_column}")
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
    except (DatasetValidationError, DuplicateError) as e:
        print(e)
        sys.exit(1)
