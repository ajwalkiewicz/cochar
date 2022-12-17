# __main__.py
import argparse

from . import cochar


def pars_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        type=int,
        required=False,
        default=cochar.YEAR,
        help="Character's year of born",
    )
    parser.add_argument(
        "--first_name",
        type=str,
        required=False,
        default=cochar.FIRST_NAME,
        help="Character's first name",
    )
    parser.add_argument(
        "--last_name",
        type=str,
        required=False,
        default=cochar.LAST_NAME,
        help="Character's last name",
    )
    parser.add_argument(
        "--age",
        type=int,
        required=False,
        default=cochar.AGE,
        help="Character's age",
    )
    parser.add_argument(
        "--sex",
        type=str,
        required=False,
        default=cochar.SEX,
        dest="sex",
        help="Character's sex",
    )
    parser.add_argument(
        "--country",
        type=str,
        required=False,
        default=cochar.COUNTRY,
        choices=["US", "PL", "ES"],
        help="Character's country",
    )
    parser.add_argument(
        "--occupation",
        type=str,
        required=False,
        default=cochar.OCCUPATION,
        help="Character's occupation",
    )
    parser.add_argument(
        "--occup_type",
        type=str,
        required=False,
        default=cochar.OCCUPATION_TYPE,
        choices=["classic", "expansion", "custom"],
        help="Occupation type",
    )
    parser.add_argument(
        "--era",
        type=str,
        required=False,
        default=cochar.ERA,
        choices=["classic-1920", "modern"],
        help="Occupation era",
    )
    parser.add_argument(
        "--tags",
        type=str,
        required=False,
        default=cochar.TAGS,
        choices=["lovecraftian", "criminal"],
        help="Occupation tags",
    )

    return parser.parse_args()


def main():
    args = pars_arguments()
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
    except cochar.error.NoneOccupationMeetsCriteria as e:
        print(e)


if __name__ == "__main__":
    main()
