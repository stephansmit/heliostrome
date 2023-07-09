.PHONY: check_os clean build docs help
.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
    # Set environment variable for Windows
    OS_TYPE := windows
else ifeq ($(shell uname -s),Linux)
	# Set environment variable for Linux
	OS_TYPE := linux
else ifeq ($(shell uname -s),Darwin)
	# Set environment variable for macOS
	OS_TYPE := macos
else
	# Set environment variable for other operating systems
	OS_TYPE := other
endif
export OS_TYPE


define BROWSER_PYSCRIPT
import os, webbrowser, sys;from urllib.request import pathname2url;webbrowser.open('file://' + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER :=  python -c "$(BROWSER_PYSCRIPT)"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

check_os: ## check operating system
	@echo "Operating System: $(OS_TYPE)"

clean:  ## clean all build, python, and testing files
ifeq ($(OS_TYPE),windows)
	if exist rmdir /s /q build\
	if exist rmdir /s /q dist\
	if exist rmdir /s /q .eggs\
	for /R %%G in (*.egg-info) do @if exist "%%G" rmdir /s /q "%%G"
	for /R %%G in (*.egg) do @if exist "%%G" del /f /q "%%G"
	for /R %%G in (*.pyc) do @if exist "%%G" del /f /q "%%G"
	for /R %%G in (*.pyo) do @if exist "%%G" del /f /q "%%G"
	for /R %%G in (*~) do @if exist "%%G" del /f /q "%%G"
	for /D /R %%G in (__pycache__) do @if exist "%%G" rmdir /s /q "%%G"
	if exist rmdir /s /q .tox> NUL\
	if exist rmdir /s /q .coverage>NUL\
	if exist rmdir /s /q coverage.xml>NUL\
	if exist rmdir /s /q htmlcov>NUL\
	if exist rmdir /s /q .pytest_cache>NUL
else
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr .tox/
	rm -fr .coverage
	rm -fr coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache
endif

build: ## run tox / run tests and lint
	tox

gen-docs: ## generate Sphinx HTML documentation, including API docs
ifeq ($(OS_TYPE),windows)
	if exist rmdir /s /q docs\heliostrome*.rst
	if exist rmdir /s /q docs\modules.rst
else
	rm -f docs/heliostrome*.rst
	rm -f docs/modules.rst	
endif
	sphinx-apidoc -o docs/ heliostrome **/tests/
	$(MAKE) -C docs html

docs: ## generate Sphinx HTML documentation, including API docs, and serve to browser
	make gen-docs
	$(BROWSER) docs/_build/html/index.html
