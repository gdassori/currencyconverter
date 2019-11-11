set -e

venv/bin/coverage run --source=src -m unittest discover tests
venv/bin/coverage html
venv/bin/coverage report
