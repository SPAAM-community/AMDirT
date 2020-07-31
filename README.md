# AncientMetagenomeDirCheck

A python package to check AncientMetagenomeDir.

AncientMetagenomeDirCheck will verify the dataset against the json schema

## Install

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
  Homepage & Documentation: github.com/maxibor/ancientMetagenomeDirCheck

  DATASET: path to tsv file of dataset to check
  SCHEMA: path to JSON schema file

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```
