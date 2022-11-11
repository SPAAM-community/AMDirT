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
    accessions,
    remote,
    markdown,
    verbose,
):
    if not verbose:
        warnings.filterwarnings("ignore")
    v = AMDirValidator(schema, dataset)
    if validity:
        v.validate_schema()
    if duplicate:
        v.check_duplicate_rows()
    if columns:
        v.check_columns()
    if doi:
        v.check_duplicate_dois()
    if multi_values:
        v.check_multi_values(column_names=multi_values)
    if accessions:
        v.check_sample_accession(remote=remote)
    if markdown:
        v.to_markdown()
    else:
        v.to_rich()
