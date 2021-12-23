[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4003826.svg)](https://doi.org/10.5281/zenodo.4003826) [![PyPI version](https://badge.fury.io/py/AMDirT.svg)](https://pypi.org/project/AMDirT)

# AMDirT

AMDirT: [AncientMetagenomeDir](https://github.com/spaAM-community/ancientmetagenomedir) Toolkit

## Install

### From PyPI using pip

```bash
pip install AMDirT
```

### The latest development version, directly from GitHub

```bash
pip install --upgrade --force-reinstall git+https://github.com/spaAM-community/AMDirT.git@dev
```

## Documentation

```bash
AMDirT --help
Usage: AMDirT [OPTIONS] COMMAND [ARGS]...

  AMDirT: Performs validity check of ancientMetagenomeDir datasets
  Author: Maxime Borry
  Contact: <maxime_borry[at]eva.mpg.de>
  Homepage & Documentation: github.com/spaam-workshop/AMDirT


Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  convert       Converts filtered samples and libraries tables to eager...
  filter        Launch interactive filtering tool
  test-dataset  Run validity check of ancientMetagenomeDir datasets...
```
```bash
$ AMDirT test-dataset --help
Usage: AMDirT test-dataset [OPTIONS] DATASET SCHEMA

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
$ AMDirT filter --help
Usage: AMDirT filter [OPTIONS]

  Launch interactive filtering tool

Options:
  -t, --tables PATH  JSON file listing AncientMetagenomeDir tables
  --help             Show this message and exit.
```
```bash
$ AMDirT convert --help
Usage: AMDirT convert [OPTIONS] SAMPLES TABLE_NAME

  Converts filtered samples and libraries tables to eager and fetchNGS input tables

  SAMPLES: path to filted samples tsv file
  TABLE_NAME: name of table to convert

Options:
  -t, --tables PATH       JSON file listing AncientMetagenomeDir tables
  -o, --output DIRECTORY  conversion output directory
  --help                  Show this message and exit.
```
