import os

from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="python-fieldclimate",
    version="0.1dev",
    packages=["fieldclimate"],
    package_data={"": ["*.txt", "*.rst"]},
    author="Agrimanagent, Inc.",
    author_email="pmarshall@agrimgt.com",
    description="A client for the iMetos FieldClimate API.",
    long_description=read("README.rst"),
    license="MIT",
    project_urls={"Official Documentation": "https://api.fieldclimate.com/v1/docs/"},
)
