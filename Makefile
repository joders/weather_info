PYTHON = python3

.PHONY = test run clean

FILES = app.py

.DEFAULT_GOAL = run

test:
	${PYTHON} -m pytest
	
run:
	FLASK_APP=app.py flask run -h 0.0.0.0

clean:
	rm -r __pycache__
