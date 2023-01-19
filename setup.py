import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = ''

setuptools.setup(
    name="stairstep",
    version="0.1.1-tra",
    author="Adam Gilman",
    author_email="oss+stairstep@adamgilman.com",
    description="A Pythonic API for Amazon's States Language for defining AWS Step Functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adamgilman/stairstep",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
