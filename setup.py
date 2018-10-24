import os

from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="python-fieldclimate",
    version="0.1dev",
    description="A client for the iMetos FieldClimate API.",
    url="https://github.com/agrimgt/python-fieldclimate",
    long_description=read("README.rst"),
    author="Agrimanagent, Inc.",
    author_email="pmarshall@agrimgt.com",
    license="MIT",
    project_urls={
        "API Documentation": "https://api.fieldclimate.com/v1/docs/",
        "Source": "https://github.com/agrimgt/python-fieldclimate",
    },
    packages=["fieldclimate"],
    install_requires=["aiohttp", "pycryptodome", "requests"],
    python_requires=">=3.6",
    package_data={"": ["*.txt", "*.rst"]},
)
