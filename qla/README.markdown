# Quantum Linear Algebra

Minimal library intended to learn the linear algebra required to understand quantum computing concepts.

No dependency other than my multiple dispatch module. Slow, no numpy, Numba, Taichi...

Build with
```bash
pip3 wheel .
```
To specify dependencies not found in the pypi repositories use the full git URL in `setup.py`:

```python
# setup.py
   setup(
    ... 
    install_requires=[
        "dyn-dispatch @ https://github.com/uv-python/modules/raw/main/modules/dyn_dispatch-0.4-py3-none-any.whl"],
    ...)
```
