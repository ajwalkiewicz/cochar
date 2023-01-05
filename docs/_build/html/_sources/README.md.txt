[![PyPI version](https://badge.fury.io/py/cochar.svg)](https://badge.fury.io/py/cochar)
[![License: GNU GPL v3](https://img.shields.io/badge/License-GNU%20GPL%20v3-red.svg)](https://github.com/ajwalkiewicz/cochar/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://shields.io/)
[![Author: Walu](https://img.shields.io/badge/Aurhor-Walu-gray.svg)](https://shields.io/)

# **C**all **O**f **C**thulhu C**har**acter Generator

Fast way of creating a random character for Call of Cthulhu RPG 7th ed.

## Summary

`cochar` stands for `Call of Cthulhu Character`. It's a python package design to create a full characters for Call of Cthulhu RPG 7th ed.

A sample power `cochar` package can be observed on [www.cochar.pl](www.cochar.pl)

## Table of Contents

- [Project Title](#call-of-cthulhu-character-generator)
- [Summary](#summary)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Documentation](#documentation)
- [Contribution](#contribution)
- [Web version](#web-version)
- [Author](#author)
- [License](#license)

## Installation

```
pip3 install cochar
```

## Usage

### Basic

Example:

```Python
>>> from cochar import create_character
>>> person = create_character(1925, "US")
>>> person
>>> Character(year=1925, country='US', first_name='Anthem', last_name='Pharr', age=22, sex='M', occupation='doctor of medicine', strength=33, condition=30, size=78, dexterity=40, appearance=23, education=87, intelligence=65, power=50, move_rate=7, luck=38, skills={'first aid': 38, 'language [latin]': 9, 'medicine': 73, 'science [biology]': 48, 'ride': 64, 'anthropology': 6, 'charm': 46, 'intimidate': 32, 'art/craft (sculptor)': 9, 'credit rating': 74, 'doge': 20}, damage_bonus='0', build=0, doge=20, sanity_points=50, magic_points=10, hit_points=10)
```

### Default settings

Default settings are defined in `./data/settings.json`.

```json
{
  "min_age": 15,
  "max_age": 90,
  "max_skill_level": 90,
  "year": 1925,
  "age": null,
  "sex": null,
  "first_name": null,
  "last_name": null,
  "country": "US",
  "occupation": null,
  "weights": true,
  "database": "",
  "show_warnings": false,
  "occupation_type": null,
  "era": null,
  "tags": null
}
```

## Dependencies

`cochar` depends on [randname](https://github.com/ajwalkiewicz/randname) module for generating random names.

For more details please see:

- [randname github](https://github.com/ajwalkiewicz/randname)
- [randname pypi](https://pypi.org/project/rname/)

## Documentation

Detailed documentation of module can by found here:
[cochar documentation](https://ajwalkiewicz.github.io/cochar/_build/html/index.html#)

## Contribution

If you want to contribute to `cochar` project read [contribution](https://github.com/ajwalkiewicz/cochar/blob/main/CONTRIBUTION.md) for more information.

## Web Version

> Web application is not a part of `cochar` package.

Web application was design to present the power of `cochar` package. You can check it out on [www.cochar.pl](www.cochar.pl)

## Author

Adam Walkiewicz

## License

Cochar is licensed under the terms of the [GNU GPL v3](https://github.com/ajwalkiewicz/cochar/blob/main/LICENSE)
