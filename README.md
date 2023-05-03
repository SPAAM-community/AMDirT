[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4003825.svg)](https://doi.org/10.5281/zenodo.4003825) [![PyPI version](https://badge.fury.io/py/AMDirT.svg)](https://pypi.org/project/AMDirT) [![Documentation Status](https://readthedocs.org/projects/amdirt/badge/?version=dev)](https://amdirt.readthedocs.io/en/dev/?badge=dev) [![AMDirT-CI](https://github.com/SPAAM-community/AMDirT/actions/workflows/ci_test.yml/badge.svg)](https://github.com/SPAAM-community/AMDirT/actions/workflows/ci_test.yml)

# AMDirT

**AMDirT**: [**A**ncient**M**etagenome**Dir**](https://github.com/SPAAM-community/ancientmetagenomedir) **T**oolkit

AMDirT is a toolkit for interacting with the AncientMetagenomeDir metadata repository of ancient metagenomic samples and ancient microbial genomes. This tool provides ways to validate AncientMetagenomeDir submissions, explore and download sequencing data for ancient microbial and environmental (meta)genomes, and automatically prepare input samplesheets for a range of bioinformatic processing pipelines.

For documentation on using the tool, please see [How Tos](how_to/index), [Tutorials](/tutorials) and/or [Quick Reference](/reference).

## Install

### 1. With pip

```bash
pip install amdirt
```

### 2. With conda

```bash
conda install -c bioconda amdirt
```

### The latest development version, directly from GitHub

```bash
pip install --upgrade --force-reinstall git+https://github.com/SPAAM-community/AMDirT.git@dev
```

### The latest development version, with local changes

- Fork AMDirT on GitHub
- Clone your fork `git clone [your-AMDirT-fork]`
- Checkout the `dev` branch `git switch dev`
- Create the conda environment `conda env create -f environment.yml`
- Activate the environment `conda activate amdirt`
- Install amdirt in development mode `pip install -e .`
  - In some cases you may need to force update streamlit with `pip install --upgrade steamlit`

To locally render documentation:

- `conda activate amdirt`
- Install additional requirements `cd docs && pip install -r requirements.txt`
- Build the HTML `make html`
- Open the `build/html/README.html` file in your browser

## More information

For more information, please see the AMDirT Documentation

- Stable: [amdirt.readthedocs.io/en/latest/](https://amdirt.readthedocs.io/en/latest/)
- Development version: [amdirt.readthedocs.io/en/dev/](https://amdirt.readthedocs.io/en/dev/)
