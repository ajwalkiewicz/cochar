[![PyPI version](https://badge.fury.io/py/cochar.svg)](https://badge.fury.io/py/cochar)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://shields.io/)
[![Author: Walu](https://img.shields.io/badge/Aurhor-Walu-gray.svg)](https://shields.io/)

# <u>**C**</u>all <u>**O**</u>f <u>**C**</u>thulhu C<u>**har**</u>acter Generator

Fast way of creating a random character for Call of Cthulhu RPG 7th ed.

## Summary

`cochar` stands fo `Call of Cthulhu Character`. It's a python module design to create a full characters for Call of Cthulhu RPG 7th ed.

## Table of Contents

- [Project Title](#call-of-cthulhu-character-generator)
- [Summary](#summary)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Documentation](#documentation)
- [Contribution](#contribution)
- [Authors & Contributors](#authors-&-contributors)
- [TODO](#todo)
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
Character(year=1925, country='US', first_name='Anthem', last_name='Pharr', age=22, sex='M', occupation='doctor of medicine', strength=33, condition=30, size=78, dexterity=40, appearance=23, education=87, intelligence=65, power=50, move_rate=7, luck=38, skills={'first aid': 38, 'language [latin]': 9, 'medicine': 73, 'science [biology]': 48, 'ride': 64, 'anthropology': 6, 'charm': 46, 'intimidate': 32, 'art/craft (sculptor)': 9, 'credit rating': 74, 'doge': 20}, damage_bonus='0', build=0, doge=20, sanity_points=50, magic_points=10, hit_points=10)
```

### Default settings

Default settings are defined in `./data/settings.json`.

```json
{
  "min_age": 15,
  "max_age": 90,
  "max_skill_level": 90,
  "year": 1925,
  "age": false,
  "sex": false,
  "first_name": false,
  "last_name": false,
  "country": "US",
  "occupation": "optimal",
  "weights": true,
  "database": "",
  "show_warnings": false
}
```

## Dependencies

`cochar` depends on [randname](github.com/ajwalkiewicz/randname) module for generating random names.

For more details please see:

- [randname github](github.com/ajwalkiewicz/randname)
- [randname pypi](https://pypi.org/project/rname/)

## Documentation

Detailed documentation of module can by found here:
[cochar documentation](https://ajwalkiewicz.github.io/cochar/_build/html/index.html#)

## Contribution

If you want to contribute to `cochar` project read [contribution](CONTRIBUTION.md) for more information.

## Authors & Contributors

**Author**: Adam Walkiewicz

**Contributors**: Be first!

## TODO

List of things that I'd like to add or improve. Those are rather long term goals, not something that I'm working on.

### Module

1. [ ] Move skills to separate json file
2. [ ] More occupations
3. [ ] Historically accurate mode: occupations and skills depending on year of the game. Age limit for some professions like fo doctor or professor.

### Webapp

1. [ ] Export character to character sheet
2. [ ] Face generator

## License

Cochar is licensed under the terms of the [GNU GPLv3](LICENSE)
