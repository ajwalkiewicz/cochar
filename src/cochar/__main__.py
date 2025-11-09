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
import argparse
from collections.abc import Sequence

import cochar.cochar as cochar
import cochar.config as config
import cochar.error as error


def parse_arguments(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        type=int,
        required=False,
        default=config.YEAR,
        help="Character's year of born",
    )
    parser.add_argument(
        "--first_name",
        type=str,
        required=False,
        default=config.FIRST_NAME,
        help="Character's first name",
    )
    parser.add_argument(
        "--last_name",
        type=str,
        required=False,
        default=config.LAST_NAME,
        help="Character's last name",
    )
    parser.add_argument(
        "--age",
        type=int,
        required=False,
        default=config.AGE,
        help="Character's age",
    )
    parser.add_argument(
        "--sex",
        type=str,
        required=False,
        default=config.SEX,
        dest="sex",
        help="Character's sex",
    )
    parser.add_argument(
        "--country",
        type=str,
        required=False,
        default=config.COUNTRY,
        choices=["US", "PL", "ES"],
        help="Character's country",
    )
    parser.add_argument(
        "--occupation",
        type=str,
        required=False,
        default=config.OCCUPATION,
        help="Character's occupation",
    )
    parser.add_argument(
        "--occup_type",
        type=str,
        required=False,
        default=config.OCCUPATION_TYPE,
        choices=["classic", "expansion", "custom"],
        help="Occupation type",
    )
    parser.add_argument(
        "--era",
        type=str,
        required=False,
        default=config.ERA,
        choices=["classic-1920", "modern"],
        help="Occupation era",
    )
    parser.add_argument(
        "--tags",
        type=str,
        required=False,
        default=config.TAGS,
        choices=["lovecraftian", "criminal"],
        help="Occupation tags",
    )

    return parser.parse_args(args)


def main():
    args = parse_arguments()
    if args.tags:
        tags = [args.tags]
    else:
        tags = args.tags
    try:
        print(
            cochar.create_character(
                year=args.year,
                first_name=args.first_name,
                last_name=args.last_name,
                age=args.age,
                sex=args.sex,
                country=args.country,
                occupation=args.occupation,
                occup_type=args.occup_type,
                era=args.era,
                tags=tags,
            )
        )
    except error.NoneOccupationMeetsCriteria as e:
        print(e)


if __name__ == "__main__":
    main()
