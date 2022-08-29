import cochar
from cochar import error
from flask import Flask, render_template, url_for, Response, jsonify, abort
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# API

get_args = reqparse.RequestParser(bundle_errors=True)
get_args.add_argument(
    "year", default=1925, type=int, help="Year of the game as integer", location="args"
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
    help="Country in alpha-2 code format",
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
    default=False,
    type=str,
    choices=("M", "F"),
    help="{error_msg}. For random choice omit this parameter",
    location="args",
)
get_args.add_argument(
    "occupation", default="optimal", type=str, case_sensitive=False, location="args"
)
get_args.add_argument(
    "mode", default="full", type=str, case_sensitive=False, location="args"
)

# Data Validation
# TODO: Data validation on server side

# Response to request


class GenerateCharacter(Resource):
    def get(self):
        try:
            kwargs = get_args.parse_args()
            character = cochar.create_character(**kwargs)
            return character.get_json_format(kwargs["mode"].lower())
        except error.CocharError as e:
            return {"status": "fail", "message": str(e)}
            # return abort(400, description=str(e))


api.add_resource(GenerateCharacter, "/api/get")

# Errors
# @app.errorhandler(400)
# def error_400(Exception):
#     return , 400

# Main Page


@app.route("/")
@app.route("/generator")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/donation")
def donation():
    return render_template("donation.html")


if __name__ == "__main__":
    app.run(debug=True)
