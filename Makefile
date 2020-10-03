deploy:
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --skip-existing dist/*

.phony: deploy
