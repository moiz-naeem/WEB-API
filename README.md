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

### Requirements
* SQLAlchemy
* Flask
* Flask-SQLAlchemy

### Additional requirements for running tests
* pytest

To install depencies run to following:
```bash
pip install -r requirements.txt
```

To install the Librerian as Python package run the following
```
pip install -e .
```

### Testing

To test database run the following (this requires Librerian as package)
```
pytest tests/db_test.py --verbose
```
