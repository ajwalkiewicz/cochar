# **C**all **O**f **C**thulhu **Char**acter Generator

Fast way of creating a random character for Chall of Cthulhu RPG 7th ed. 

## Summary

`cochar` stands fo `Call of Cthulhu Character`. It's a python module desing to create a full characters for Call of Cthulgu RPG 7th ed.

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
- [To Do](#to-do)
- [License](#license)

## Installation

```
pip3 install cochar
```

## Usage

### Basic

Example:

```Python
from cochar import Character
c = Character()
Character(age=30, sex='M', first_name='Kelvin', last_name='Burlingame', country='US', occupation='antiquarian', characteristics={'str': 57, 'con': 23, 'siz': 75, 'dex': 23, 'app': 80, 'edu': 87, 'int': 48, 'pow': 18, 'move_rate': 7}, luck=33, skills={'appraise': 64, 'history': 90, 'library use': 90, 'spot hidden': 90, 'listen': 27, 'persuade': 89, 'pilot': 9, 'sleight of hand': 12, 'credit rating': 69, 'doge': 11}, weights=True, damage_bonus='+1K4', build=1, doge=11)
```

### Avanced 

You can set any of the following parameters to create Character object:

    year (int, optional) – year when character born, defaults to 1925

    age (str, optional) – character age, defaults to None

    sex (str, optional) – character sex, defaults to None

    first_name (str, optional) – character name, random if not set, defaults to None

    last_name (str, optional) – character last name, random if not set, defaults to None

    country (str, optional) – country to generate name and last name, defaults to “US”

    occupation (str, optional) – character occupation, optimal occupation (base on max skill points) if not set, defaults to “optimal”

    occupation_points (int, optional) – occupation point, max if not set, defaults to None

    hobby_points (int, optional) – hobby points, 2*intelligence if not set, defaults to None

    skills (dict, optional) – character skills, random if not set, defaults to None

    strength (int, optional) – character strength, random if not set, defaults to 0

    condition (int, optional) – character condition, random if not set, defaults to 0

    size (int, optional) – character size, random if not set, defaults to 0

    dexterity (int, optional) – character dexterity, random if not set, defaults to 0

    apperance (int, optional) – character apperance, random if not set, defaults to 0

    edducation (int, optional) – character edducation, random if not set, defaults to 0

    intelligence (int, optional) – character intelligence, random if not set, defaults to 0

    power (int, optional) – character power, random if not set, defaults to 0

    move_rate (int, optional) – character move_rate, random if not set, defaults to 0

    sanity_points (int, optional) – character sanity_points, random if not set, defaults to 0

    magic_points (int, optional) – character magic_points, random if not set, defaults to 0

    hit_points (int, optional) – character hit_points, random if not set, defaults to 0

    luck (int, optional) – character luck, random if not set, default to 0

## Dependencies

`cochar` depends on [randname](github.com/ajwalkiewicz/randname) module for generating random names.

For more details please see: 
- [randname github](github.com/ajwalkiewicz/randname)
- [randname pypi](https://pypi.org/project/rname/)

## Documentation

Detailed documentation of module can by found here:
[cochar documentation](https://ajwalkiewicz.github.io/cochar/_build/html/index.html#)

## Contribution

If you want to contribute to `cochar` projcet read [contribution](CONTRIBUTION.md) for more information.

## Authors & Contributors

**Author**: Adam Walkiewicz

**Contributors**: Be first!

## To do

### Basic improvements

1. [ ] Move occupation to extrnal files
2. [ ] Write more thorough unit tests
3. [ ] Save characters feature
4. [ ] Simple GUI 
5. [ ] Add custom Errors
6. [ ] Add more suited occupations for NPC's

### Dream improvements

Realisticaly those improvement probably will never be introduced. 

1. [ ] Generating PDF's
2. [ ] Interactive and advance graphical GUI

## License

Cochar is licensed under the terms of the [GNU GPLv3](LICENSE)