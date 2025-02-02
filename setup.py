from setuptools import setup, find_packages

def parse_requirements(filename):
    """Load requirements from a pip requirements file"""
    with open(filename) as file:
        lines = file.read().splitlines()
    # Ignore comments and empty lines
    requirements = [line for line in lines if line and not line.startswith('#')]
    # Exclude editable installs (-e lines) since they shouldn't go in install_requires
    # requirements = [line for line in lines if line and not line.startswith('-e')]
    return requirements

setup(
    name="daas_py_api_asset",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True, 
    author="Neal Routson",
    author_email="nroutson@gmail.com",
    description="Django API for managing assets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nealrout/daas_py_api_asset",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    install_requires=parse_requirements('requirements.txt'),
)
