import cochar
import markdown
import os
from cochar import error
from flask import (
    Flask,
    Response,
    abort,
    jsonify,
    render_template,
    url_for,
    request,
    make_response,
)
from flask_restful import Api, Resource, reqparse


_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
_README = os.path.abspath(os.path.join(_THIS_FOLDER, "static", "README.md"))

with open(_README, "r", encoding="utf-8") as readme:
    text = readme.read()
    html = markdown.markdown(text)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

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

get_advanced_args = reqparse.RequestParser(bundle_errors=True)

get_advanced_args.add_argument(
    "era", default="classic-1920", type=str, case_sensitive=False, location="args"
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
                **kwargs
            )
            return character.get_json_format()
        except error.CocharError as e:
            return {"status": "fail", "message": str(e)}


api.add_resource(GenerateCharacter, "/api/get")

# Errors


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", version=cochar.__version__), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", version=cochar.__version__), 404


# Main Page


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", version=cochar.__version__)


@app.route("/generator")
def generator():
    return render_template("generator.html", version=cochar.__version__)


@app.route("/docs")
def about():
    return render_template("docs.html", version=cochar.__version__)


@app.route("/donation")
def donation():
    return render_template("donation.html", version=cochar.__version__)


@app.route("/faq")
def faq():
    return "Work in progress"


@app.route("/news")
def news():
    return "Work in progress!"


# Tests


@app.route("/tests")
def tests():
    # user_agent = request.headers.get("User-Agent")
    # return f"<p>Your browser is {user_agent}</p>"
    # return render_template("test.html", tests=html)
    # response = make_response(render_template("test.html", name=html))
    # response.set_cookie("privacy_policy", "1")
    # return response
    return render_template("test.html", python_module=html, version=cochar.__version__)


if __name__ == "__main__":
    app.run(debug=True)
