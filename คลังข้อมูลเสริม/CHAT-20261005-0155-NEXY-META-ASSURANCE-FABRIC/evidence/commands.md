# Reproducible Evidence Commands

Executed from package root:

```bash
PYTHONPATH=src python3 -m compileall -q src tests
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Static hidden-I/O audit parsed all Python source with `ast` and rejected imports in:

```text
os sys subprocess socket requests urllib http random time datetime pathlib sqlite3
multiprocessing threading asyncio
```

Raw observed outputs are stored in this directory. The source/test SHA-256 manifest identifies the aligned artifacts used for the final local execution.
