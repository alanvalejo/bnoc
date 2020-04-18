TEST = PYTHONPATH=$(pwd):$(PYTHONPATH) pytest -v tests

test:
	$(TEST)

# to enable terminal output such as by using print:
test-dev:
	$(TEST) -s


# still not enabled, needs publication into PyPI:
pip-install:
	sudo pip3 install bnoc

# working, misses the requirements, though:
pip-local-install:
	sudo pip3 install -e .
