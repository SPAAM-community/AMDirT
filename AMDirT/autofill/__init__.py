from typing import AnyStr
from AMDirT.core import logger
from AMDirT.core.diff import get_sample_diff
from AMDirT.validate.application import AMDirValidator
from AMDirT.core.ena import ENAPortalAPI


def run_autofill(local: AnyStr, remote: AnyStr, schema: AnyStr):
    """Generate library metadata table from a list of archive
    accessions and corresponding secondary_sample_accessions

    Args:
            accessions (list): ENA project accessions
            sec_accessions (list): ENA secondary_sample_accessions

    Returns:
            pd_frame: data frame of library metadata
    """

    local_validator = AMDirValidator(
        schema=schema,
        dataset=local,
    )

    remote_validator = AMDirValidator(
        schema=schema,
        dataset=remote,
    )
    diff = get_sample_diff(
        local=local_validator.dataset,
        remote=remote_validator.dataset,
        schema=local_validator.schema,
    )  # This returns a tuple with a list of samples

    e = ENAPortalAPI()

    for sample in diff[0]:
        api_result = e.query(
            sample,
            fields=[
                "first_public",
                "sample_alias",
                "study_accession",
                "secondary_sample_accession",
                "library_name",
                "instrument_platform",
                "library_layout",
                "library_strategy",
                "read_count",
                "run_accession",
                "sra_ftp",
                "sra_md5",
            ],
        )
