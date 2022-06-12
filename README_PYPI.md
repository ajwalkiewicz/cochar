# **C**all **O**f **C**thulhu **Char**acter Generator

Fast way of creating a random character for Chall of Cthulhu RPG 7th ed. 

## Summary

`cochar` stands fo `Call of Cthulhu Character`. It's a python module desing to create a full characters for Call of Cthulgu RPG 7th ed.

## Installation

```
pip3 install cochar
```

## Basic Usage

Example:

```Python
from cochar import Character
c = Character()
Character(age=30, sex='M', first_name='Kelvin', last_name='Burlingame', country='US', occupation='antiquarian', characteristics={'str': 57, 'con': 23, 'siz': 75, 'dex': 23, 'app': 80, 'edu': 87, 'int': 48, 'pow': 18, 'move_rate': 7}, luck=33, skills={'appraise': 64, 'history': 90, 'library use': 90, 'spot hidden': 90, 'listen': 27, 'persuade': 89, 'pilot': 9, 'sleight of hand': 12, 'credit rating': 69, 'doge': 11}, weights=True, damage_bonus='+1K4', build=1, doge=11)
```

## Dependencies

`cochar` depends on [randname](github.com/ajwalkiewicz/randname) module for generating random names.

For more details please see: 
- [randname github](github.com/ajwalkiewicz/randname)
- [randname pypi](https://pypi.org/project/rname/)

## Documentation

Detailed documentation of module can by found here:
[cochar documentation](https://ajwalkiewicz.github.io/cochar/_build/html/index.html#).

## Contribution

If you want to contribute to `cochar` projcet read [contribution](CONTRIBUTION.md) for more information.

## Authors & Contributors

**Author**: Adam Walkiewicz

**Contributors**: Be first!

## License

Cochar is licensed under the terms of the [GNU GPLv3](LICENSE)