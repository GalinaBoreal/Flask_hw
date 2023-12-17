import pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from models import Session, Advt
from schema import CreateAdvt, UpdateAdvt


app = Flask("app")
bcrypt = Bcrypt(app)


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error ": error.description})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


def get_advt_by_id(advt_id: int):
    user = request.session.get(Advt, advt_id)
    if user is None:
        raise HttpError(404, "advt not found")
    return user


def add_advt(advt: Advt):
    try:
        request.session.add(advt)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "advt already exists")
    return advt


class AdvtView(MethodView):
    def get(self, advt_id: int):
        advt = get_advt_by_id(advt_id)
        return jsonify(advt.json)

    def post(self):
        json_data = validate(CreateAdvt, request.json)
        advt = Advt(**json_data)
        add_advt(advt)
        response = jsonify(advt.json)
        response.status_code = 201
        return response

    def patch(self, advt_id: int):
        json_data = validate(UpdateAdvt, request.json)
        advt = get_advt_by_id(advt_id)
        for field, value in json_data.items():
            setattr(advt, field, value)
            add_advt(advt)
        return jsonify(advt.json)

    def delete(self, advt_id: int):
        advt = get_advt_by_id(advt_id)
        request.session.delete(advt)
        request.session.commit()
        return jsonify({"status": "success"})


advt_view = AdvtView.as_view("advt_view")

app.add_url_rule(
    "/advt",
    view_func=advt_view,
    methods=["POST"],
)
app.add_url_rule(
    "/advt/<int:advt_id>", view_func=advt_view, methods=["GET", "PATCH", "DELETE"]
)

if __name__ == "__main__":
    app.run(debug=True)
