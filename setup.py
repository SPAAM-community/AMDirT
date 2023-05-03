from setuptools import setup, find_packages
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="AMDirT",
    version=get_version("AMDirT/__init__.py"),
    description="AMDirT: AncientMetagenomeDir Toolkit",
    long_description=open("README.md").read(),
    url="https://github.com/SPAAM-community/AMDirT",
    long_description_content_type="text/markdown",
    license="GNU-GPLv3",
    python_requires=">=3.9",
    install_requires=[
        "click",
        "pandas",
        "tabulate",
        "jsonschema",
        "rich",
        "streamlit",
        "streamlit-aggrid",
        "numpy",
        "requests",
        "colorlog"
    ],
    packages=find_packages(exclude="test"),
    entry_points={"console_scripts": ["AMDirT = AMDirT.cli:cli"]},
    package_dir={"AMDirT": "AMDirT"},
    package_data={"AMDirT.assets": ["tables.json"]},
)
