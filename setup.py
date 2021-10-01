import os
from setuptools import setup

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

with open(f"{THIS_FOLDER}/README_PYPI.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cochar",
    version="0.1.0",
    description="Call of Cthulhu character generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajwalkiewicz/cochar",
    project_urls={
        "Documentation": "https://ajwalkiewicz.github.io/cochar/_build/html/index.html"
        },
    author="Adam Walkiewicz",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        # "Programming Language :: Python :: 3.6",
        # "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["cochar"],
    include_package_data=True,
    install_requires=[
        "rname"
    ],
    # packages=find_packages("src"),
    # package_dir={'': 'src'},
    # package_data={'': ['data/USA/fisrs_names/*']},
    # data_file=[('data', ['USA/fisrs_names/*'])],
    entry_points={
        "console_scripts": [
            "cochar=cochar.__main__:main"
        ]
    }
)
