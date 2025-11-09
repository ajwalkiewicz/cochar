<!--
Cochar - create a random character for Call of Cthulhu RPG 7th ed.
Copyright (C) 2025  Adam Walkiewicz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
# How-To Guides

## Using Make in This Project

This project uses `make` to automate various tasks. Below are the available commands and their descriptions:

### Setup
To set up the project, run:
```sh
make setup
```
This will check if `uv` is installed and set up the project environment.

### Build
To build the project, run:
```sh
make build
```
This will check the code, run tests, and build the package.

### Test
To run the tests, use:
```sh
make test
```
This will run the tests excluding those marked as slow.

To run all tests, use:
```sh
make test_all
```

### Clean
To clean the project, run:
```sh
make clean
```
This will remove the virtual environment, build files, and cache.

### Format
To format the project files, run:
```sh
make format
```
This will format the files using `ruff`.

### Check
To check the project files, run:
```sh
make check
```
This will check the files using `ruff`.

### Type Checking
To check the typing, run:
```sh
make type
```
This will check the typing using `mypy`.

### Documentation
To build the documentation, run:
```sh
make docs
```

To serve the documentation locally, run:
```sh
make docs_serve
```

To upload the documentation, run:
```sh
make docs_upload
```