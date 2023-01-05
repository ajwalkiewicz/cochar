import os
from setuptools import setup

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

with open(f"{THIS_FOLDER}/docs/readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cochar",
    version="1.0.0-alpha.5",
    description="Call of Cthulhu character generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # long_description_content_type="text/x-rst",
    url="https://github.com/ajwalkiewicz/cochar",
    project_urls={
        "Documentation": "https://ajwalkiewicz.github.io/cochar/_build/html/index.html"
    },
    author="Adam Walkiewicz",
    license="GPL 3.0",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        # "Programming Language :: Python :: 3.6",
        # "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["cochar"],
    include_package_data=True,
    install_requires=["rname"],
    # packages=find_packages("src"),
    # package_dir={'': 'src'},
    entry_points={"console_scripts": ["cochar=cochar.__main__:main"]},
)
