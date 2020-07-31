import pandas as pd
import json
from jsonschema import validate
from io import StringIO
from ancientMetagenomeDirCheck.exceptions import DatasetValidationError, DuplicateError


def check_validity(dataset, schema):
    dt = pd.read_csv(dataset, sep="\t")
    dt_json = json.load((StringIO(dt.to_json(orient="records"))))

    with open(schema, "r") as j:
        json_schema = json.load(j)

    validate(instance=dt_json, schema=json_schema)


def run_tests(dataset, schema):
    check_validity(dataset, schema)
