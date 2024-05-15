# PWP SPRING 2024
# LIBRERIAN
Create your own library and share books with others

# Group information
* Student 1. Moiz  mulrehma23@student.oulu.fi
* Student 2. Mikki mihiltun23@student.oulu.fi
* Student 3. Santeri lharju@student.oulu.fi

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

## README checklist
- Dependencies (external libraries)
- How to setup the framework.
- How to populate and setup the database.
- How to setup (e.g. modifying any configuration files) and run your RESTful API.
- The URL to access your API (usually nameofapplication/api/version/)=> the path to your application.
- Instructions on how to run the different tests for your application.

## Implementation Details
### Database
Database used is SQLite, check wiki for database schema.

### Dependencies
Librerian depends on the following python packages
- flask
- flask_sqlalchemy
- flask_restful
- sqlalchemy
- jsonschema
- flasgger
- pyyaml
- requests
- pytest
- pylint

## Setup and Usage
Recommended way to run 
Create Python virtual enviroment
```bash
python3 -m venv venv
```

Set enviroment variables in the activate script that you will be using 
```bash
echo "export FLASK_APP=librerian" >> venv/bin/activate
echo "export FLASK_ENV=develpoment" >> venv/bin/activate
```

Activate virtual enviroment and install required packages
```bash
source venv/bin/activate
pip install -r requirements.txt
```
Initialize the database 
```bash
flask init-db
```
And optionally generate dummy data for testing
```bash
flask gen-db
```
Now you can run Flask app using
```bash
flask run
```


### Running tests

To run Pytest, it is required to install the Librerian as Python package
```bash
pip install -e .
```
Afterwhich pytest and pylint can be run

```bash
pytest tests
pylint librerian
```
