import os
import re
import sys

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 9)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(f"""
==========================
Unsupported Python version
==========================
This version of Slightly Better Types requires Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}, but you're trying
to install it on Python {CURRENT_PYTHON[0]}.{CURRENT_PYTHON[1]}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install slightly-better-types
This will install the latest version of Slightly Better Types which works on
your version of Python. If you can't upgrade your pip (or Python), request
an older version of Slightly Better Types:
    $ python -m pip install "slightly-better-types<3.10"
""")
    sys.exit(1)


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('slightly_better_types')

setuptools.setup(
    name="slightly-better-types",
    version=version,
    author="Peter Wensel",
    author_email="pwensel@gmail.com",
    url="https://github.com/slightly-better-python/slightly-better-types",
    description="Improved abstraction for dealing with union and named types.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires='>=3.9',
    install_requires=[]
)
