###


### Installation

install poetry ()link

Then, you can activate the python environment as
```bash
poetry env use 3.11
poetry shell
poetry update # to load the dependencies.
```

To run the application, simply
```bash
docker build -t m-y .
docker run -d -p 8000:8000 m-y
```

Test with some example requests:
```bash
python -m unittest app/requests/py_examples.py
```