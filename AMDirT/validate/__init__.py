from distutils.log import warn
from AMDirT.validate.application import AMDirValidator
import warnings


def run_validation(
    dataset,
    schema,
    validity,
    duplicate,
    columns,
    doi,
    multi_values,
    markdown,
    verbose,
):
    if not verbose:
        warnings.filterwarnings("ignore")
    v = AMDirValidator(schema, dataset)
    if validity and v.parsing_ok:
        v.validate_schema()
    if duplicate and v.parsing_ok:
        v.check_duplicate_rows()
    if columns and v.parsing_ok:
        v.check_columns()
    if doi and v.parsing_ok:
        v.check_duplicate_dois()
    if multi_values and v.parsing_ok: 
        v.check_multi_values(column_names=multi_values)
    if markdown:
        v.to_markdown()
    else:
        v.to_rich()
