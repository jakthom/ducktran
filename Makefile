.PHONY: install ipython

install:
	pdm install

ipython:
	.venv/bin/ipython;
