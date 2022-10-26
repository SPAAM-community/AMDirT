import json
import pandas as pd
from AMDirT.validate import exceptions
from io import StringIO
from pathlib import Path
from rich.table import Table
from rich.console import Console
from dataclasses import dataclass
from jsonschema import Draft7Validator, exceptions as json_exceptions
from typing import AnyStr, BinaryIO, TextIO, Union, Tuple

Schema = Union[AnyStr, BinaryIO, TextIO]
Dataset = Union[AnyStr, BinaryIO, TextIO]


@dataclass
class DFError:
    error: str
    source: str
    column: str
    row: str
    message: str

    def to_dict(self):
        return {
            "Error": str(self.error),
            "Source": str(self.source),
            "Column": str(self.column),
            "Row": str(self.row),
            "Message": str(self.message),
        }

    def to_list(self):
        return [
            str(i)
            for i in [self.error, self.source, self.column, self.row, self.message]
        ]


class DatasetValidator:
    def __init__(self, schema: Schema, dataset: Dataset):
        self.schema = self.read_schema(schema)
        self.schema_name = Path(schema).name
        self.dataset = self.read_dataset(dataset)
        self.dataset_name = Path(dataset).name
        self.dataset_json = self.dataset_to_json()
        self.errors = list()

    def __repr__(self):
        return (
            f"DatasetValidator(schema={self.schema_name}, dataset={self.dataset_name})"
        )

    def add_error(self, err: DFError):
        self.errors.append(err)

    def read_schema(self, schema: Schema) -> dict:
        """Read JSON schema from file or string
        Args:
            schema (str): Path to schema in json format
        Returns:
            dict: JSON schema
        """

        with open(schema, "r") as s:
            return json.load(s)

    def read_dataset(self, dataset: Dataset) -> pd.DataFrame:
        """ "Read dataset from file or string
        Args:
            dataset (str): Path to dataset in tsv format
        Returns:
            pd.DataFrame: Dataset as pandas dataframe
        """
        try:
            return pd.read_table(dataset, sep="\t")
        except pd.errors.ParserError as e:
            self.add_error(
                DFError(
                    "Dataset Parsing Error", self.dataset_name, None, None, e.message
                )
            )

    def check_columns(self):
        """Checks if dataset has all required columns"""
        col_diff = set(self.dataset.columns).difference(
            set(self.schema["items"]["required"])
        )
        try:
            if col_diff != 0:
                raise exceptions.ColumnDifferenceError(
                    f"Dataset has different columns compared to schema {col_diff}"
                )
        except exceptions.ColumnDifferenceError as e:
            for c in col_diff:
                self.add_error(DFError(e.name, c, None, None, e.message))

    def dataset_to_json(self) -> dict:
        """Convert dataset from Pandas DataFrame to JSON
        Returns:
            dict: Dataset as dictionary
        """
        return json.load((StringIO(self.dataset.to_json(orient="records"))))

    def validate_schema(self):
        """Validate dataset against JSON schema"""
        validator = Draft7Validator(self.schema)
        for err in validator.iter_errors(self.dataset_json):
            self.add_error(self.cleanup_errors(err))

    def cleanup_errors(self, error: json_exceptions.ValidationError) -> DFError:
        """Cleans up JSON schema validation errors
        Args:
            error (json_exceptions.ValidationError): JSON schema validation error
        Returns:
            list[error instance, error line, error column, error message]: Cleaned up error
        """
        err_column = list(error.path)[-1]
        if "enum" in error.schema:
            if len(error.schema["enum"]) > 3:
                error.message = f"'{error.instance}' is not an accepted value.\nPlease check [link={self.schema['items']['properties'][err_column]['$ref']}]{self.schema['items']['properties'][err_column]['$ref']}[/link]"
        err_line = str(error.path[0] + 2)
        return DFError(
            "Schema Validation Error",
            error.instance,
            err_line,
            err_column,
            error.message,
        )

    def check_duplicate_rows(self):
        """Checks for duplicated rows in dataset"""
        try:
            dup_df = self.dataset[self.dataset.duplicated(keep=False)]
            if len(dup_df) > 0:
                dup_rows = (
                    dup_df.groupby(dup_df.columns.tolist(), dropna=False)
                    .apply(lambda x: tuple(x.index))
                    .tolist()
                )
                raise exceptions.DuplicateError(f"Rows \n{dup_rows} are duplicated")
        except exceptions.DuplicateError as e:
            for r in dup_rows:
                self.add_error(DFError(e.name, r, None, r, f"Rows {r} are duplicated"))

    def to_rich(self):
        """Generate output table

        Args:
            columns (list): name of columns
            rows (list of list): rows of the table
            title (str): title of the table
            method (string): table generation method (rich or markdown)
        """

        table = Table(
            title=f"AMDirT Validation Report of {self.dataset_name} against {self.schema_name}"
        )
        columns = ["Error", "Source", "Column", "Row", "Message"]
        for column in columns:
            table.add_column(column, style="red", overflow="fold")
        for error in self.errors:
            table.add_row(*(error.to_list()))

        console = Console()
        console.print(table)

    def to_markdown(self):
        df = pd.DataFrame(columns=["Error", "Source", "Column", "Row", "Message"])
        for error in self.errors:
            df = df.append(
                error.to_dict(),
                ignore_index=True,
            )
        return df.to_markdown(index=False)


if __name__ == "__main__":

    s = "/Users/maxime/Documents/github/AMDirT/test/data/schema.json"
    d = "/Users/maxime/Documents/github/AMDirT/test/data/invalid.tsv"

    v = DatasetValidator(s, d)
    v.validate()
    v.check_columns()
    v.check_duplicate_rows()
    v.to_rich()
    print(v.errors)
    print(v.to_markdown())
