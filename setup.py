import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-mdb",
    version="0.0.1a1",
    author="Ryan Zembrodt",
    author_email="ryan.zembrodt@gmail.com",
    description="Package for parsing IMDb datasets and scraping web pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zembrodt/pymdb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)