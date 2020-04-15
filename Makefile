TEST = PYTHONPATH=$(pwd):$(PYTHONPATH) pytest -v tests

test:
	$(TEST)

# to enable terminal output such as by using print:
test-dev:
	$(TEST) -s
