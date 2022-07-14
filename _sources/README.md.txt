[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4003826.svg)](https://doi.org/10.5281/zenodo.4003826) [![PyPI version](https://badge.fury.io/py/AMDirT.svg)](https://pypi.org/project/AMDirT) [![Documentation Status](https://readthedocs.org/projects/amdirt/badge/?version=dev)](https://amdirt.readthedocs.io/en/dev/?badge=dev)

# AMDirT

**AMDirT**: [**A**ncient**M**etagenome**Dir**](https://github.com/SPAAM-community/ancientmetagenomedir) **T**oolkit

## Install

Before we release AMDirt on (bio)Conda, please follow the instructions below.

### 1. Install the conda environment and activate it

```bash
conda env create -f environment.yml
conda activate amdirt
```

### The latest development version, directly from GitHub

```bash
pip install --upgrade --force-reinstall git+https://github.com/SPAAM-community/AMDirT.git@dev
```

### From PyPI using pip (only the code on master branch)

```bash
pip install AMDirT
```

### The latest development version, with local changes

From within you local clone of the AMDirT repository

```bash
pip install -e .
```

## Documentation

- Stable: [amdirt.readthedocs.io/en/latest/](https://amdirt.readthedocs.io/en/latest/)
- Development version: [amdirt.readthedocs.io/en/dev/](https://amdirt.readthedocs.io/en/dev/)
