
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="darwin",
    version="0.1.0",
    author="Lorenzo",
    author_email="zetatez@icloud.com",
    description="darwin trading api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zetatez/darwin",
    packages=["darwin"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OSX",
    ],
    python_requires='>=3.8',
)
