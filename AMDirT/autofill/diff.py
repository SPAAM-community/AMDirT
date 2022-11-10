import itertools
from AMDirT.validate.application import AMDirValidator
from typing import AnyStr, Tuple


def get_sample_diff(local: AnyStr, remote: AnyStr, schema: AnyStr) -> Tuple[AnyStr]:
    """Returns a diff of the two files.

    Args:
        local: The local file path.
        remote: The remote file path.
        schema: The schema file path.

    Returns:
        tuple: A set of the sample only present locally.
    """

    local_validator = AMDirValidator(
        schema=schema,
        dataset=local,
    )
    remote_validator = AMDirValidator(
        schema=schema,
        dataset=remote,
    )

    remote_samples = set(
        itertools.chain.from_iterable(
            [i.split(",") for i in remote_validator.dataset["archive_accession"]]
        )
    )

    local_samples = set(
        itertools.chain.from_iterable(
            [i.split(",") for i in local_validator.dataset["archive_accession"]]
        )
    )

    return tuple(local_samples.difference(remote_samples))
