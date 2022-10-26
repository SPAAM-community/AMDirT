from AMDirT.validate.application import AMDirValidator


def run_validation(
    dataset,
    schema,
    validity,
    duplicate,
    doi,
    markdown,
):
    v = AMDirValidator(schema, dataset)
    if validity:
        v.validate_schema()
    if duplicate:
        v.check_duplicate_rows()
    if doi:
        v.check_duplicate_dois()
    if markdown:
        v.to_markdown()
    else:
        v.to_rich()
