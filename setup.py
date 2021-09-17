from pathlib import Path

from setuptools import setup

setup(
    long_description=(Path(__file__) / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
