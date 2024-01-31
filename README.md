# End to end ML Project

Project setup:

1. Download and install Anaconda: https://www.anaconda.com/download
2. Setup a virtual env using conda cli: `conda create -n <envname> python=3.12`
3. Activate the env: `conda activate <envname>`
4. Install `poetry`: `python -m pip install poetry`
5. Install all dependencies using `poetry` cli: `poetry install`
6. Run the mlflow server: `mlflow server`, run the prefect server: `prefect server start`
7. Run the project: `python main.py`

To make it work, we need to do a quick hack:

in `<condaenvname>/lib/python3.12/importlib/metadata/__init__.py/`

Add a method `get()` to the class `EntryPoints(tuple)`:

```python
def get(self, name, default):
    try:
        return self.__getitem__(name)
    except Exception:
        return default
```

in Windows conda, the location of the file most likely is:

`C:\Users\<YourUserName>\anaconda3\envs\<condaenvname>\Lib\importlib\metadata\__init__.py`
