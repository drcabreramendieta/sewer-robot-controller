# Getting Started
1. Create a venv with Python 3.10 or above.
2. Install all the dependencies with:
```bash
pip install -r requirements.txt
```
3. Add the src directory to PYTHONPATH with:
```bash
export PYTHONPATH=src
```

# Class diagram generation
The code has been refactored for an easy class-diagram generation by pyreverse. For a container (a.k.a module), it is made by:
```bash
pyreverse -f ALL src/<container>/
```
for example
```bash
pyreverse -f ALL src/Communication/
```
generates the class-diagram of the Communication container. For more advances options, check the [pyreverse documentation](https://pylint.readthedocs.io/en/latest/additional_tools/pyreverse/configuration.html). Also, many containers can be included in the generation like this:
```bash
pyreverse -f ALL src/Video src/Communication/ src/Panel_and_Feeder/ src/Inspection/
```