rm -f dist/red_dead_tools-*.whl dist/red-dead-tools-*.tar.gz
python setup.py sdist bdist_wheel
twine upload dist/*
