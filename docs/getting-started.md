<!--
Cochar - create a random character for Call of Cthulhu RPG 7th ed.
Copyright (C) 2023  Adam Walkiewicz

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

# Getting Started

## Installation

To install the package, use pip:

```sh
pip install cochar
```

## Basic Usage

The simplest way to create a character is to use the `create_character` function with just the year and country:

```python
from cochar import create_character

# Create a random character for 1925 in the United States
character = create_character(1925, "US")
print(character)
```

This will generate a complete character with random attributes, skills, occupation, and personal details.

## Creating a Character with Specific Parameters

You can customize character creation by providing specific parameters:

```python
from cochar import create_character

# Create a character with specific attributes
character = create_character(
    year=1925,
    country="US",
    age=35,
    sex="F",
    first_name="Sarah",
    last_name="Thompson",
    occupation="doctor of medicine"
)

print(f"Name: {character.first_name} {character.last_name}")
print(f"Age: {character.age}, Sex: {character.sex}")
print(f"Occupation: {character.occupation}")
print(f"Skills: {character.skills}")
```

## Available Parameters

The `create_character` function accepts the following parameters:

- `year` (required): The year in which the game takes place
- `country` (required): The character's country of origin (e.g., "US")
- `first_name`: Character's first name (random if not provided)
- `last_name`: Character's last name (random if not provided)
- `age`: Character's age (random within valid range if not provided)
- `sex`: Character's sex - "M" or "F" (random if not provided)
- `occupation`: Character's occupation (random based on characteristics if not provided)
- `random_mode`: If True, choose occupation completely randomly regardless of statistics
- `occup_type`: Filter occupations by type
- `era`: Filter occupations by era
- `tags`: Filter occupations by tags

## Accessing Character Attributes

Once created, you can access various character attributes:

```python
character = create_character(1925, "US")

# Personal information
print(f"Name: {character.first_name} {character.last_name}")
print(f"Age: {character.age}, Sex: {character.sex}")
print(f"Occupation: {character.occupation}")

# Characteristics
print(f"Strength: {character.strength}")
print(f"Dexterity: {character.dexterity}")
print(f"Intelligence: {character.intelligence}")
print(f"Education: {character.education}")

# Derived attributes
print(f"Hit Points: {character.hit_points}")
print(f"Sanity Points: {character.sanity_points}")
print(f"Magic Points: {character.magic_points}")
print(f"Damage Bonus: {character.damage_bonus}")

# Skills
print(f"Skills: {character.skills}")
print(f"Dodge: {character.dodge}")
```

## Working with Different Time Periods

You can create characters for different eras by changing the year:

```python
# 1920s character
character_1920s = create_character(1925, "US")

# Modern era character
character_modern = create_character(2020, "US")
```

## Command Line Usage

You can also use cochar from the command line:

```sh
python3 -m cochar
```

This will launch an interactive character generation session.

## Next Steps

- Check out the [Documentation](documentation.md) for detailed API reference
- See [Contribution](contribution.md) if you'd like to contribute to the project
- Visit the web version at [www.cochar.pl](http://www.cochar.pl) to see cochar in action