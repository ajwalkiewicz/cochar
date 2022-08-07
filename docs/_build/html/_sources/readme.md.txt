# **C**all **O**f **C**thulhu **Char**acter Generator

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
>>> from cochar import create_character
>>> person = create_character(1925, "US")
>>> person
Character(year=1925, country='US', first_name='Anthem', last_name='Pharr', age=22, sex='M', occupation='doctor of medicine', strength=33, condition=30, size=78, dexterity=40, appearance=23, education=87, intelligence=65, power=50, move_rate=7, luck=38, skills={'first aid': 38, 'language [latin]': 9, 'medicine': 73, 'science [biology]': 48, 'ride': 64, 'anthropology': 6, 'charm': 46, 'intimidate': 32, 'art/craft (sculptor)': 9, 'credit rating': 74, 'doge': 20}, damage_bonus='0', build=0, doge=20, sanity_points=50, magic_points=10, hit_points=10)
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

If you want to contribute to `cochar` projcet read [contribution](CONTRIBUTION.md) for more information.

## Authors & Contributors

**Author**: Adam Walkiewicz

**Contributors**: Be first!

## To do

### Basic improvements

1. [ ] Move occupation to external files
2. [ ] Write more thorough unit tests
3. [ ] Save characters feature
4. [ ] Simple GUI 
5. [ ] Add custom Errors
6. [ ] Add more suited occupations for NPC's

### Dream improvements

Realistically those improvement probably will never be introduced. 

1. [ ] Generating PDF's
2. [ ] Interactive and advance graphical GUI

## License

Cochar is licensed under the terms of the [GNU GPLv3](LICENSE)