# End to end ML Project

To make it work, we need to do a quick hack:

in `<condaenvname>/lib/python3.12/importlib/metadata/__init__.py/`

Add a method `get()` to the class `EntryPoints(tuple)`:

```
def get(self, name, default):
    try:
        return self.__getitem__(name)
    except Exception:
        return default
```
