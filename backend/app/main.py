import os
from typing import NoReturn

from flask import Flask, Response

from app.apis.todo import make_todos_blueprint
from app.repository.base import Repository
from app.repository.postgres import PostgresRepository


def main() -> None:
    repository = PostgresRepository.factory()
    repository.connect()
    try:
        repository.initialize()
        run_flask_app(repository)
    finally:
        repository.disconnect()


def run_flask_app(repository: Repository) -> NoReturn:
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = os.environ.get("FLASK_PORT", 5000)

    app = Flask(__name__)
    app.after_request(_cors_support)
    app.register_blueprint(make_todos_blueprint(repository))
    app.run(host=host, port=port)


def _cors_support(response: Response) -> Response:
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    return response


if __name__ == "__main__":
    main()
