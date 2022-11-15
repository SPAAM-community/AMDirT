import json
from numpy import int64
import pandas as pd
from AMDirT.validate import exceptions
from AMDirT.core import logger
from io import StringIO
from pathlib import Path
from rich.table import Table
from rich.console import Console
from dataclasses import dataclass
from jsonschema import Draft7Validator, exceptions as json_exceptions
from typing import AnyStr, BinaryIO, TextIO, Union

Schema = Union[AnyStr, BinaryIO, TextIO]
Dataset = Union[AnyStr, BinaryIO, TextIO]


@dataclass
class DFError:
    """Class to store DataFrame validation errors"""

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
    """Dataset as DataFrame validation class"""

    def __init__(self, schema: Schema, dataset: Dataset):
        self.errors = list()
        self.dataset_name = Path(dataset).name
        self.schema_name = Path(schema).name
        self.schema = self.read_schema(schema)
        self.dataset = self.read_dataset(dataset,self.schema)
        self.dataset_json = self.dataset_to_json()

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

    def read_dataset(self, dataset: Dataset, schema: dict) -> pd.DataFrame:
        """ "Read dataset from file or string
        Args:
            dataset (str): Path to dataset in tsv format
            schema (dict): Parsed schema as dictionary (from read_schema)
        Returns:
            pd.DataFrame: Dataset as pandas dataframe
        """
        string_to_dtype_conversions = {
            'string': str,
            'integer': pd.Int64Dtype(),
        }
        column_dtypes = {}
        for column_keys in schema['items']['properties']:
            coltype = schema['items']['properties'][column_keys]['type'][0]
            if coltype in string_to_dtype_conversions:
                column_dtypes[column_keys] = string_to_dtype_conversions[coltype]
            elif coltype == 'null':
                self.add_error(
                    DFError(
                        error = "Schema Error",
                        source = column_dtypes[column_keys],
                        column = column_keys,
                        row = None,
                        message = "Default/first type of column in schema can not be null"
                    )
                )
                raise SystemExit
            else:
                column_dtypes[column_keys] = coltype
        try:
            return pd.read_table(dataset, sep="\t", dtype=column_dtypes)
        except (AttributeError, pd.errors.ParserError, ValueError) as e:
            logger.error(e)
            self.add_error(
                DFError(
                    "Dataset Parsing Error",
                    self.dataset_name,
                    None,
                    None,
                    e,
                )
            )
            raise SystemExit

    def check_columns(self) -> bool:
        """Checks if dataset has all required columns

        Returns:
            bool: True if dataset has all required columns, False otherwise
        """
        col_diff = set(self.dataset.columns).difference(
            set(self.schema["items"]["required"])
        )
        try:
            if len(col_diff) != 0:
                raise exceptions.ColumnDifferenceError(
                    f"Dataset has different columns compared to schema {col_diff}"
                )
            else:
                return True
        except exceptions.ColumnDifferenceError as e:
            for c in col_diff:
                self.add_error(DFError(e.name, c, None, None, e.message))
            return False

    def dataset_to_json(self) -> dict:
        """Convert dataset from Pandas DataFrame to JSON

        Returns:
            dict: Dataset as dictionary
        """
        return json.load((StringIO(self.dataset.to_json(orient="records"))))

    def validate_schema(self) -> bool:
        """Validate dataset against JSON schema

        Returns:
            bool: True if dataset is valid, False otherwise
        """
        validator = Draft7Validator(self.schema)
        # redefining json type 'null' to accept python None as correct instance of 'null'
        validator.TYPE_CHECKER.redefine('null',lambda validator,instance: instance is None)
        err_cnt = 0
        for err in validator.iter_errors(self.dataset_json):
            self.add_error(self.cleanup_errors(err))
            err_cnt += 1
        if err_cnt > 0:
            return False
        else:
            return True

    def cleanup_errors(self, error: json_exceptions.ValidationError) -> DFError:
        """Cleans up JSON schema validation errors

        Args:
            error (json_exceptions.ValidationError): JSON schema validation error
        Returns:
            DFError: Cleaned DataFrame error
        """
        err_column = list(error.path)[-1]
        if "enum" in error.schema:
            if len(error.schema["enum"]) > 3:
                error.message = f"'{error.instance}' is not an accepted value.\nPlease check [link={self.schema['items']['properties'][err_column]['$ref']}]{self.schema['items']['properties'][err_column]['$ref']}[/link]"
        err_line = str(error.path[0] + 2)
        return DFError(
            "Schema Validation Error",
            error.instance,
            err_column,
            err_line,
            error.message,
        )

    def check_duplicate_rows(self) -> bool:
        """Checks for duplicated rows in dataset

        Returns:
            bool: True if dataset has no duplicated rows, False otherwise
        """
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
            return False
        return True

    def to_rich(self):
        """Generate rich output table for console display

        Returns:
            bool: True if dataset is valid
        Raises:
            SystemExit: If dataset is invalid
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
        if len(self.errors) > 0:
            console.print(table)
            raise SystemExit(f"Invalid dataset {self.dataset_name}")
        else:
            logger.info(f"{self.dataset_name} is valid")
            return True

    def to_markdown(self) -> bool:
        """Generate markdown output table for github display

        Returns:
            bool: True if dataset is valid
        Raises:
            SystemExit: If dataset is invalid
        """
        df = pd.DataFrame(columns=["Error", "Source", "Column", "Row", "Message"])
        for error in self.errors:
            df = df.append(
                error.to_dict(),
                ignore_index=True,
            )
        if len(df) > 0:
            raise SystemExit(
                f"Invalid dataset `{self.dataset_name}`\n\n{df.to_markdown(index=False)}"
            )
        else:
            logger.info(f"{self.dataset_name} is valid")
            return True
