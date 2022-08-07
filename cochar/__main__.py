# __main__.py
import argparse

from . import cochar


def pars_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        type=int,
        required=False,
        default=1925,
        # dest="year",
        help="Characte's year of born",
    )
    parser.add_argument(
        "--first_name",
        type=str,
        required=False,
        default=False,
        # dest="first_name",
        help="Character's first name",
    )
    parser.add_argument(
        "--last_name",
        type=str,
        required=False,
        default=False,
        # dest="last_name",
        help="Character's last name",
    )
    parser.add_argument(
        "--age",
        type=int,
        required=False,
        default=False,
        # dest="age",
        help="Character's age",
    )
    parser.add_argument(
        "--sex",
        type=str,
        required=False,
        default=False,
        dest="sex",
        help="Characte's sex",
    )
    parser.add_argument(
        "--country",
        type=str,
        required=False,
        default="US",
        # dest="country",
        help="Characte's cauntry",
    )
    parser.add_argument(
        "--occupation",
        type=str,
        required=False,
        default="optimal",
        # dest='occupation',
        help="Characte's occupation",
    )
    return parser.parse_args()


def main():
    args = pars_arguments()
    print(
        cochar.create_character(
            year=args.year,
            first_name=args.first_name,
            last_name=args.last_name,
            age=args.age,
            sex=args.sex,
            country=args.country,
            occupation=args.occupation,
        )
    )


if __name__ == "__main__":
    main()
