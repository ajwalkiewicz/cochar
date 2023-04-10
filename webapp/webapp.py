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

import os

import markdown
from flask import Flask, render_template, request
from flask_limiter import Limiter, RateLimitExceeded
from flask_restful import Api, Resource, reqparse

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import cochar
import cochar.occup
from cochar import error

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
_README = os.path.abspath(os.path.join(_THIS_FOLDER, "static", "README.md"))

OCCUPATIONS = cochar.occup.get_occupation_list()
LIMITS = ["10 per second", "10000 per day"]

def get_remote_address() -> str:
    """Get client's IP address.
    pythonanywhere.com stores original client's IP in 'X-Real-IP' header.
    Without it `request.remote_addr` returns internal load-balancer IP and
    FlaskLimiter blocks all requests world wide.

    :return: client's IP address
    :rtype: str
    """
    return request.headers.get('X-Real-IP') or request.remote_addr or "127.0.0.1"


with open(_README, "r", encoding="utf-8") as readme:
    text = readme.read()
    html = markdown.markdown(text)

app = Flask(__name__)

api = Api(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri="memory://",
)

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

get_advanced_args = reqparse.RequestParser(bundle_errors=True)

get_advanced_args.add_argument(
    "era",
    default="classic-1920",
    type=str,
    case_sensitive=False,
    location="args",
)
get_advanced_args.add_argument(
    "occup_type",
    default=None,
    type=str,
    choices=("classic", "expansion", "custom", None),
    location="args",
)
get_advanced_args.add_argument(
    "tags",
    default=None,
    type=str,
    choices=("lovecraftian", "criminal", None),
    location="args",
)

# Data Validation
# TODO: Data validation on server side

# API


class GenerateCharacter(Resource):
    def get(self):
        try:
            with limiter.limit(";".join(LIMITS)):
                kwargs = get_args.parse_args()
                advanced_args = get_advanced_args.parse_args()

                era = advanced_args.era.split(",")

                if advanced_args.tags:
                    tags = advanced_args.tags.split(",")
                else:
                    tags = advanced_args.tags

                occup_type = advanced_args.occup_type

                cochar.SKILLS_INTERFACE.era = era
                skills_generator = cochar.skill.SkillsGenerator(cochar.SKILLS_INTERFACE)

                character = cochar.create_character(
                    era=era,
                    tags=tags,
                    occup_type=occup_type,
                    skills_generator=skills_generator,
                    **kwargs,
                )
                return character.get_json_format()
        except error.CocharError as e:
            return {"status": "fail", "origin": "cochar", "message": str(e)}, 400
        except RateLimitExceeded:
            return {
                "status": "fail",
                "origin": "flask_limiter",
                "message": (
                    f"Exceeded limit of requests: {os.linesep}{os.linesep.join(LIMITS)}"
                    "\nPlease try again later.\n"
                    "If you did not exceed the limit check if someone "
                    "else in your network is using this website"
                    )
            }, 429


api.add_resource(GenerateCharacter, "/api/v1/get")

# Errors


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", version=cochar.__version__), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", version=cochar.__version__), 500


# Main Page


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", version=cochar.__version__)


@app.route("/generator")
def generator():
    return render_template(
        "generator.html", occupations=OCCUPATIONS, version=cochar.__version__
    )


@app.route("/docs")
def docs():
    return render_template(
        "docs.html",
        python_module=html,
        occupations=OCCUPATIONS,
        version=cochar.__version__,
    )


@app.route("/donation")
def donation():
    return render_template("donation.html", version=cochar.__version__)


@app.route("/canceled")
def canceled():
    return render_template("canceled.html", version=cochar.__version__)


@app.route("/completed")
def completed():
    return render_template("completed.html", version=cochar.__version__)


@app.route("/faq")
def faq():
    return render_template("faq.html", version=cochar.__version__)


@app.route("/news")
def news():
    return "Work in progress!"


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host="0.0.0.0", debug=True)
