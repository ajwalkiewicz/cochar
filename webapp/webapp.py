import cochar
import markdown
import os
from cochar import error
from flask import Flask, Response, abort, jsonify, render_template, url_for
from flask_restful import Api, Resource, reqparse

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
_README = os.path.abspath(os.path.join(_THIS_FOLDER, "static", "README.md"))

with open(_README, "r", encoding="utf-8") as readme:
    text = readme.read()
    html = markdown.markdown(text)

app = Flask(__name__)
api = Api(app)


# API

get_args = reqparse.RequestParser(bundle_errors=True)
get_args.add_argument(
    "year",
    default=1925,
    type=int,
    help="{error_msg}. Year mus be an integer number.",
    location="args",
)
get_args.add_argument(
    "first_name",
    default=False,
    type=str,
    help="Character's first name",
    location="args",
)
get_args.add_argument(
    "last_name", default=False, type=str, help="Character's last name", location="args"
)
get_args.add_argument(
    "country",
    default="US",
    type=str,
    choices=("US", "PL", "ES"),
    help="Bad choice: {error_msg}. Country in alpha-2 code format. Available countries: 'US', 'PL', 'ES'",
    location="args",
)
get_args.add_argument(
    "age",
    default=False,
    type=int,
    help="Age must be an integer: {error_msg}",
    location="args",
)
get_args.add_argument(
    "sex",
    default=None,
    type=str,
    choices=("M", "F"),
    help="Bad choice: {error_msg}. For random choice omit this parameter",
    location="args",
)
get_args.add_argument(
    "random_mode", default=False, type=bool, case_sensitive=False, location="args"
)
get_args.add_argument(
    "occupation", default="", type=str, case_sensitive=False, location="args"
)

# Data Validation
# TODO: Data validation on server side

# Response to request


class GenerateCharacter(Resource):
    def get(self):
        try:
            kwargs = get_args.parse_args()

            occup_era = ["classic-1920"]
            skills_era = ["classic-1920"]
            cochar.SKILLS_INTERFACE.era = skills_era
            SKILLS_GENERATOR = cochar.skill.SkillsGenerator(cochar.SKILLS_INTERFACE)

            character = cochar.create_character(
                era=occup_era, skills_generator=SKILLS_GENERATOR, **kwargs
            )
            return character.get_json_format()
        except error.CocharError as e:
            return {"status": "fail", "message": str(e)}


api.add_resource(GenerateCharacter, "/api/get")

# Errors
# @app.errorhandler(400)
# def error_400(Exception):
#     return , 400

# Main Page


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/generator")
def generator():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/donation")
def donation():
    return render_template("donation.html")


@app.route("/faq")
def faq():
    return "Work in progress"


@app.route("/news")
def news():
    return "Work in progress"


@app.route("/tests")
def tests():
    return html


if __name__ == "__main__":
    app.run(debug=True)
