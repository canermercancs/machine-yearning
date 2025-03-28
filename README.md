###


### Installation

install poetry 
```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
pipx install poetry
```

Then, you can activate the python environment as
```bash
poetry env use 3.11
poetry shell
poetry update # to load the dependencies.
```

```bash
poetry add <dependency>
```

To run the application, simply
```bash
docker build -t m-y .
docker run -d -p 8000:8000 m-y
# Test with some example requests on another terminal:
python -m unittest app/requests/py_examples.py
```