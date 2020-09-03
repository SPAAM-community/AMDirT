[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4003826.svg)](https://doi.org/10.5281/zenodo.4003826) [![PyPI version](https://badge.fury.io/py/ancientMetagenomeDirCheck.svg)](https://pypi.org/project/ancientMetagenomeDirCheck)

# AncientMetagenomeDirCheck

A python package to check AncientMetagenomeDir.

AncientMetagenomeDirCheck will verify a dataset, in tabular format, against a json schema.

## Install

### From PyPI using pip

```bash
pip install ancientMetagenomeDirCheck
```

### The latest development version, directly from GitHub

```bash
pip install --upgrade --force-reinstall git+https://github.com/SPAAM-workshop/AncientMetagenomeDirCheck.git
```

## Documentation

```bash
$ ancientMetagenomeDirCheck --help
Usage: ancientMetagenomeDirCheck [OPTIONS] DATASET SCHEMA

  ancientMetagenomeDirCheck: Performs validity check of ancientMetagenomeDir datasets
  Author: Maxime Borry
  Contact: <borry[at]shh.mpg.de>
  Homepage & Documentation: github.com/spaam-workshop/ancientMetagenomeDirCheck

  DATASET: path to tsv file of dataset to check
  SCHEMA: path to JSON schema file

Options:
  --version        Show the version and exit.
  -v, --validity   Turn off schema checking.
  -d, --duplicate  Turn off line duplicate checking.
  -a, --accession  Turn off accession duplicate checking.
  --help           Show this message and exit.
```
