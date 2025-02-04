# daas_api_asset_python
## Project

Refrence of DaaS Project - https://github.com/nealrout/daas_docs

## Description

This is an implementation of Django to expose endpoints for the asset object.  We are purposely making the project more granular and 
not using some of the built-in features to communicate with the database.  Instead of a model, serializer,  and ModelViewSet we
are managing stored procedures in the DBMS, which the code calls.  I am doing this as a challange and to create a sepration between
application code and DBMS code.  The DB developers can have finder control over the actions coming into the DB through stored procedures.

__The Liquibase project containing DB objects:__  
https://github.com/nealrout/daas_db


## Table of Contents

- [Requirements](#requirements)
- [Uninstall-Install](#uninstall-install)
- [Usage](#usage)
- [Package](#package)
- [Features](#features)
- [Miscellaneous](#miscellaneous)
- [Contact](#contact)

## Requirements
__Set .env variables for configuration__  

ENV_FOR_DYNACONF=\<environment\>  
_i.e. development, integration, production_  

DYNACONF_SECRET_KEY=\<secret_key\>

## Uninstall-Install
__Uninstall:__  
python -m pip uninstall daas_py_api_asset

__Install:__  
python -m pip install .

__Rebuild from source:__  
python -m pip install --no-binary :all: .

## Usage
__Set correct directory:__  
cd .\asset_api\  

__Start Django api:__  
python manage.py runserver

## Package
python setup.py sdist

## Features
- List assets with pagination.
- Asset retrieve update destroy: api for updating or deleting asset records.

## Miscellaneous

### To create new virtual environment  
python -m venv myenv

### To activate the virtual environment for this project
..\.venv\Scripts\activate

### Django (notes only)
__To create a new bootstrapped projects:__  
django-admin startproject asset_api

cd asset_api  

__To create a new application:__  
python manage.py startapp assets

__To handle required migrations by built in tools:__  
python manage.py makemigrations  
python manage.py migrate

## Contact
Neal Routson  
nroutson@gmail.com