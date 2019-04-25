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

Download:
```
git clone https://github.com/Materials-Consortia/python-optimade-candidate-reference-implementation.git
```

To do some simple tests, run:
```
./start_simple_test.py
```
To just try a manual filter-type query using the example\_sqlite3 backend. This script also takes (the expression part of) an OPTIMaDe filter string as argument, so you can do, e.g.:
```
./start_simple_test.py 'id="st-6"'
```

To run everything in full 'server' mode:
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

For a more production-like deployment there is support for WSGI.
See the instructions in `start_wsgi_example_sqlite.py`

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

There are also some other examples of using parts of the provided
routines in the directory `examples/`.

Notes: 

- The parser of OPTIMaDe filter strings is relatively well-tested. 
  However, the parser output is then re-translated into a simpler 
  abstract syntax tree in src/parser/parse_optimade_filter.py
  That routine has not yet undergone heavy testing for all possible
  outcomes of the grammar, so it is possible that this function
  gets surprised by valid output of the parser and crashes.
   
- There are some unittests under `tests/`, they can be started with
  ```
  make tests
  ```
  (Look in the `Makefile` for more details.)


