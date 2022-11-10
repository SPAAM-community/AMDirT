from typing import AnyStr
from AMDirT.core import logger
from AMDirT.validate.application import AMDirValidator
from AMDirT.autofill.diff import get_sample_diff


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
