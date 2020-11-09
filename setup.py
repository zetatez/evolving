
from os import path
import setuptools

dirPath = path.abspath(path.dirname(__file__))
with open(path.join(dirPath, "README.md"), "r") as fh:
    long_description = fh.read()

PY_MODULES = ['evolving.helpers', 'evolving.tsys', 'evolving.games', 'evolving.reports', 'evolving.news']

setuptools.setup(
    name="darwin",
    version="0.1.0",
    author="Lorenzo",
    author_email="zetatez@icloud.com",
    description="darwin trading api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL",
    url="https://github.com/zetatez/darwin",
    keywords="darwin",
    install_requires=["requests"],
    packages=["darwin"],
    classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OSX",     
    ],
    python_requires='>=3.8',
)


