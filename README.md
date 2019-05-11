[![Build Status](https://travis-ci.org/Materials-Consortia/python-optimade-candidate-reference-implementation.svg?branch=master)](https://travis-ci.org/Materials-Consortia/python-optimade-candidate-reference-implementation)

Python OPTIMaDe Candidate Reference Implementation
==================================================

*Disclaimer: this code has not yet been throughly tested and should be
considered alpha quality. While this implementation has been
created in the hope that it could, eventually, become a reference
implementation of the OPTIMaDe API, at this point it does NOT
have any official endorsment by OPTIMaDe.*

Furthermore, the 'API' that is formed by the routines under `src/`
should in no sense at this point be considered stable.

This software will for the moment use version numbers
that start with the OPTIMaDe specification it implements, and then
append a version number to that. E.g., v0.9.5.1 for 
implementing v0.9.5 of the OPTIMaDe specification.

# Installation

Download:
```
git clone https://github.com/Materials-Consortia/python-optimade-candidate-reference-implementation.git
```

Dependencies:

- Python webserver serving the sqlite3 example backend: no dependencies
- Built-in Python wsgi serving of the sqlite3 example backend: no dependencies
- Other webserver, e.g., apache wsgi serving the sqlite3 example backend: apache or corresponding.
- Django serving the sqlite3 example backend: django and django-rest-framework 
- Mongodb example backend: pymongo and a running instance of mongod on localhost port 27017

# Simple test runs

Some simple tests can be run by:
```
./start_simple_test.py
```
To just try a manual filter-type query using the example\_sqlite3 backend. This script also takes (the expression part of) an OPTIMaDe filter string as argument, so you can do, e.g.:
```
./start_simple_test.py 'id="st-6"'
```

# Sqlite3 example backend

To run the sqlite3 example backend in full 'server' mode:
```
./start_serve_example_sqlite3.py
```
Then go to `http://localhost:8080/info` in your browser, and you should
see the OPTIMaDe API being served here. You can try URLs such as:
```
http://localhost:8080/structures
http://localhost:8080/calculations
http://localhost:8080/structures/st-2
http://localhost:8080/all?filter=id=%22st-2%22
http://localhost:8080/structures?filter=elements="Al"
http://localhost:8080/structures?filter=elements="Al,Ti"
```

## WSGI
For a more production-like deployment there is support for WSGI.
See the instructions in `start_wsgi_example_sqlite.py`

## Django
There is also a bare-bones implementation of serving the API
via the Django-rest-framework. Enter the `django` subdirectory
and then run the `serve_django.sh` script. You can then visit
URLs such as:
```
http://localhost:8000/structures
```
etc. It would make sense to combine this way of serving of the API
with a backend that uses Django object relational mapping rather
than a raw sqlite database and SQL queries. Such a backend is not
yet provided here.

# MongoDB example backend

To run the MongoDB example backend in full 'server' mode:
```
./start_serve_example_mongodb.py
```
Then go to `http://localhost:8080/info` in your browser, and you should
see the OPTIMaDe API being served here. You can try, e.g., the same URLs as
listed in the sqlite3 example backend section.

# Other examples

There are also some other examples of using parts of the provided
routines in the directory `examples/`.

# Validation

This implementation comes with a validator for OPTIMaDe API implementation.
You can run it with:
```
./validate_url.py url [test_name] [test_name_2] ...
```
This validates the OPTIMaDe implementation at the base url `url` and
reports any violations of the specification that it finds.

If no url is given, then the test runs against `http://localhost:8080`.
If you give optional `test_name` parameters, only those tests are run.
(The names are deduciable from running a full test). This may be useful
if one is trying to track down an error triggered by a specific test.

The unit tests automatically runs the same set of validations against all
the serving options (while simultaneously checking that running those
validations does not trigger error messages from the server processes.)

Note: only very limited validation is implemented so far.

# Unit tests

The unit tests are located under `tests/` and implemented in a way
that is compatible both with Python:s standard unittest library and
with pytest.

The testing consist of two parts:

* Running various stand-alone python scripts and checking that they
  don't generate errors (any output on stderr). This includes
  the scripts under examples/

  New tests can be created as stand-alone python scripts
  in the appropriate directory. Make sure they only print to
  stderr if an unexpected error occurs.

* Running each of the options to serve the OPTIMaDe API and
  validating them using the tests provided in the
  `src/validation` module.

  New tests are created by simply extending the src/validation
  module (including them in the all_tests array.)

To run the tests using unittest, do:
```
  make unittests
```
or, for pytest:
```
  make pytest
```

If you want to run all tests with both Python 2 and 3, you can do:
```
  make tests
```
(Look in the `Makefile` for more details on test options.)

# Final notes 

- The parser of OPTIMaDe filter strings is relatively well-tested. 
  However, the parser output is then re-translated into a simpler 
  abstract syntax tree in src/parser/parse_optimade_filter.py
  That routine has not yet undergone heavy testing for all possible
  outcomes of the grammar, so it is possible that this function
  gets surprised by valid output of the parser and crashes.

