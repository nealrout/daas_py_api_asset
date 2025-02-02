# daas_api_asset_python

## Description

This is an implementation of Django to expose endpoints for the asset object.  We are purposely making the project more granular and 
not using some of the built-in features to communicate with the database.  Instead of a model, serializer,  and ModelViewSet we
are managing stored procedures in the DBMS, which the code calls.  I am doing this as a challange and to create a sepration between
application code and DBMS code.  The DB developers can have finder control over the actions coming into the DB through stored procedures.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact

# To activate the virtual environment for this project
D:\src\GitHub\daas_api_asset_python\.venv\Scripts\activate

# To install all modules in requirements.txt
pip install -r requirements.txt
pip install -r ../daas_py_config/requirements.txt

# Django
django-admin startproject asset_api
cd asset_api
# To create a new application
python manage.py startapp assets

# To handle required migrations by built in tools.
python manage.py makemigrations
python manage.py migrate

# To start server
python manage.py runserver