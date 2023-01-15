# Cochar - create a random character for Call of Cthulhu RPG 7th ed.
# Copyright (C) 2023  Adam Walkiewicz

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
    license="AGPL v3",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        # "Programming Language :: Python :: 3.6",
        # "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=["cochar"],
    include_package_data=True,
    install_requires=["rname"],
    # packages=find_packages("src"),
    # package_dir={'': 'src'},
    entry_points={"console_scripts": ["cochar=cochar.__main__:main"]},
)
