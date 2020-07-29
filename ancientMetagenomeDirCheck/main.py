import pandas as pd
from ancientMetagenomeDirCheck.exceptions import DatasetValidationError, DuplicateError

def check_validity(standards, dataset):
    """Check validity of AncientMetagenomeDir dataset

    Args:
        standards (str): path to standards defining tsv file
        dataset (str): path to tsv file of dataset to check

    Raises:
        ValueError: Raised if column contains elements not defined in standard
    """    
    standards = pd.read_csv(standards, sep="\t")
    standard_dict = {x[0]: [y for y in x[1:] if not pd.isna(y)] for x in standards.pivot(index='Column', columns='Category', values='Category').itertuples(index=True) }
    dataset = pd.read_csv(dataset, sep="\t")

    for col in standard_dict:
        present = set([x for x in dataset[col] if str(x) != 'nan'])
        allowed = set([x for x in standard_dict[col] if str(x) != 'nan'])
        diff = present.difference(allowed)
        if len(diff) > 0:
            raise DatasetValidationError(f""""{'", "'.join([str(i) for i in list(diff)])}" not present in standards "{col}" column""")

def check_unicity(standards):
    """Check unicity of standards keys

    Args:
        standards (str): path to standards defining tsv file
    """
    standards = pd.read_csv(standards, sep="\t")
    try:
        standard_dict = {x[0]: [y for y in x[1:] if not pd.isna(y)] for x in standards.pivot(index='Column', columns='Category', values='Category').itertuples(index=True) }
    except ValueError as e:
        if "Index contains duplicate entries, cannot reshape" in str(e):
            raise DuplicateError("standards contains duplicated entries")

def run_tests(standards, dataset):
    check_unicity(standards)
    check_validity(standards, dataset)
