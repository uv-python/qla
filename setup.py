# build with: python3 setup.py bdist_wheel
from setuptools import setup, find_packages

VERSION = "0.4.1"
DESCRIPTION = "Minimal linear algebra library"
with open("README.markdown", "r") as f:
    global LONG_DESCRIPTION
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="qla",
    version="0.4.1",
    author="Ugo Varetto",
    author_email="ugovaretto@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/uv-python/qla",
    packages=find_packages(),
    install_requires=["dyn-dispatch"],
    license="BSD-3-Clause",
    keywords=["python", "math", "linear algebra", "quantum"],
)
