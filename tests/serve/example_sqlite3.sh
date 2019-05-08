#!/bin/bash

if [ -z "$1" ]; then

    python ../../start_serve_example_sqlite3.py &
    PID=$!
    
fi

echo "#### BASE URL"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     http://localhost:8080/

echo "#### STRUCTURES"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     http://localhost:8080/structures 

echo "#### CALCULATIONS"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     http://localhost:8080/calculations

echo "#### SINGLE STRUCTURE"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     http://localhost:8080/structures/testdata:cod:1000007

echo "#### STRUCTURE FILTER"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     'http://localhost:8080//structures?filter=id="testdata:cod:1000007"'

echo "#### STRUCTURE INFO"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     http://localhost:8080/structures/info

echo "#### SINGLE CALCULATION"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     http://localhost:8080/calculations/calc-3

echo "#### CALCULATION INFO"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     http://localhost:8080/calculations/info

echo "#### CALCULATION FILTER"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     'http://localhost:8080//structures?filter=id="calc-3"'


echo "#### POST QUERY ALL FOR ID=CALC-5"

curl -s --connect-timeout 5 \
     --max-time 10 \
     --retry 5 \
     --retry-delay 1 \
     --retry-max-time 40 \
     --retry-connrefuse \
     -d 'filter=id="calc-5"' -X POST http://localhost:8080/all 


if [ -n "$PID" ]; then
    kill -INT "$PID"
    wait
fi
