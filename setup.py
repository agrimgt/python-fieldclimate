from setuptools import setup

setup(
    name="python-fieldclimate",
    version="1.3",
    description="A client for the iMetos FieldClimate API.",
    url="https://github.com/agrimgt/python-fieldclimate",
    long_description="\n\n".join(
        (
            open("README.rst").read(),
            open("CHANGES.rst").read(),
            open("AUTHORS.rst").read(),
        )
    ),
    author="Agrimanagement, Inc.",
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
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=["asks", "pycryptodome"],
    python_requires=">=3.6",
    include_package_data=True,
)
