# End to end ML Project

Project setup:

1. Setup a virtual env using conda: `conda create -n <envname> python=3.12`
2. Activate the env: `conda activate <envname>`
3. Install `poetry`: `python -m pip install poetry`
4. Install all dependencies using `poetry` cli: `poetry install`
5. Run the project: `python main.py`

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
