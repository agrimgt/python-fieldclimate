from setuptools import setup

import fieldclimate


setup(
    name="python-fieldclimate",
    version=fieldclimate.__version__,
    description="A client for the iMetos FieldClimate API.",
    url="https://github.com/agrimgt/python-fieldclimate",
    long_description="\n\n".join(
        (
            open("README.rst").read(),
            open("CHANGES.rst").read(),
            open("AUTHORS.rst").read(),
        )
    ),
    author=fieldclimate.__author__,
    author_email="pmarshall@agrimgt.com",
    license="MIT",
    project_urls={"API Documentation": "https://api.fieldclimate.com/v1/docs/"},
    packages=["fieldclimate"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=["aiohttp", "pycryptodome"],
    python_requires=">=3.6",
    include_package_data=True,
)
