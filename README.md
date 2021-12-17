[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4003826.svg)](https://doi.org/10.5281/zenodo.4003826) [![PyPI version](https://badge.fury.io/py/ancientMetagenomeDirCheck.svg)](https://pypi.org/project/ancientMetagenomeDirCheck)

# AncientMetagenomeDirCheck

A python package to check AncientMetagenomeDir.

AncientMetagenomeDirCheck will verify a dataset, in tabular format, against a json schema (and some other checks...).

## Install

### From PyPI using pip

```bash
pip install ancientMetagenomeDirCheck
```

### The latest development version, directly from GitHub

```bash
pip install --upgrade --force-reinstall git+https://github.com/SPAAM-workshop/AncientMetagenomeDirCheck.git@dev
```

## Documentation

```bash
$ ancientMetagenomeDirCheck --help
Usage: ancientMetagenomeDirCheck [OPTIONS] COMMAND [ARGS]...

  ancientMetagenomeDirCheck: Performs validity check of ancientMetagenomeDir datasets
  Author: Maxime Borry
  Contact: <maxime_borry[at]eva.mpg.de>
  Homepage & Documentation: github.com/spaam-workshop/ancientMetagenomeDirCheck

  DATASET: path to tsv file of dataset to check
  SCHEMA: path to JSON schema file

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  filter        Launch interactive filtering tool
  test-dataset  Run validity check of ancientMetagenomeDir datasets...
```
```bash
$ ancientMetagenomeDirCheck test-dataset --help
Usage: ancientMetagenomeDirCheck test-dataset [OPTIONS] DATASET SCHEMA

  Run validity check of ancientMetagenomeDir datasets

  DATASET: path to tsv file of dataset to check
  SCHEMA: path to JSON schema file

Options:
  -v, --validity                  Turn on schema checking.
  -d, --duplicate                 Turn on line duplicate line checking.
  -i, --doi                       Turn on DOI duplicate checking.
  -m, --markdown                  Output is in markdown format
  -dc, --duplicated_entries TEXT  Commma separated list of columns to check
                                  for duplicated entries

  --help                          Show this message and exit.
```
```bash
$ ancientMetagenomeDirCheck filter --help
Usage: ancientMetagenomeDirCheck filter [OPTIONS]

  Launch interactive filtering tool

Options:
  -c, --config PATH  Config file to use
```
