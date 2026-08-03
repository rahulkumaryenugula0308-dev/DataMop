from setuptools import setup, find_packages

setup(
    name="datamop",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "openpyxl"
    ],
    author="Team DataMop",
    description="Automatic Data Cleaning Python Library"
)