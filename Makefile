.PHONY: all clean

all: install build run

install:
    pip3 install -r requirements.txt
run: install
    python3 main.py

build: install
    python setup.py bdist_msi

clean:
    rm -r build
    rm -r dist
    rm -r .pytest_cache

