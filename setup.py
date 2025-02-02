from setuptools import setup, find_packages

setup(
    name="daas_api_asset",
    version="0.1.0",
    author="Neal Routson",
    author_email="nroutson@gmail.com",
    description="A brief description of your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nealrout/daas_api_asset_python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",  # List your project's dependencies here
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "daas_api_asset=daas_api_asset.main:main",  # Replace with your script's entry point
        ],
    },
)
