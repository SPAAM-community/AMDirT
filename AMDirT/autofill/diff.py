import itertools
from typing import AnyStr, Tuple, Dict
from pandas import DataFrame


def get_sample_diff(local: DataFrame, remote: DataFrame, schema: Dict) -> Tuple[AnyStr]:
    """Returns a diff of the two files.

    Args:
        local: The local file path.
        remote: The remote file path.
        schema: The schema file path.

    Returns:
        tuple: A set of the sample only present locally.
    """

    remote_samples = set(
        itertools.chain.from_iterable(
            [i.split(",") for i in remote["archive_accession"]]
        )
    )

    local_samples = set(
        itertools.chain.from_iterable(
            [i.split(",") for i in local["archive_accession"]]
        )
    )

    return tuple(local_samples.difference(remote_samples))
