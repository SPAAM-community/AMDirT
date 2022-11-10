from typing import AnyStr
from AMDirT.core import logger
from AMDirT.core.diff import get_sample_diff
from AMDirT.validate.application import AMDirValidator


def run_autofill(local: AnyStr, remote: AnyStr, schema: AnyStr):

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

    logger.info("Not implemented yet")

    pass
