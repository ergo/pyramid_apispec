import random
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, exception_view_config
from pyramid_apispec.helpers import add_pyramid_paths
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

import validation


@view_config(route_name="users", renderer="json")
def users_post(request):
    """ Some comment.

    ---
    x-extension: value
    post:
      security:
        - APIKeyHeader: []
      tags:
      - "Legacy API"
      summary: "Register user"
      description: ""
      operationId: "users_post"
      consumes:
      - "application/json"
      produces:
      - "application/json"
      parameters:
      - in: "body"
        name: "body"
        description: "Foo bar"
        required: true
        schema:
          $ref: "#/definitions/FooBodySchema"
      responses:
          200:
              description: response for 200 code
              schema:
                $ref: "#/definitions/FooBodySchema"
    """
    schema = validation.FooBodySchema()
    struct = schema.loads(request.body or "{}")
    return struct.data


@view_config(route_name="bar_route", request_method="GET", renderer="json")
def bar_get(request):
    """ Return something.

    ---
    get:
        description: some description
        parameters:
          - in: query
            name: offset
            schema:
              type: integer
            description: The number of items to skip
        responses:
            200:
                description: response for 200 code
                schema:
                  $ref: "#/definitions/BarBodySchema"
    """
    return {"a_field": random.random(), "b_field": random.randint(1, 999999)}


@view_config(route_name="bar_route", request_method="POST", renderer="json")
def bar_post(request):
    """ Return something.

    ---
    post:
      tags:
      - "Other API"
      summary: "Send a list of bar's"
      description: ""
      operationId: "bar_post"
      consumes:
      - "application/json"
      produces:
      - "application/json"
      parameters:
      - in: "body"
        name: "body"
        description: "Bar body description"
        required: true
        schema:
          $ref: "#/definitions/BarBodySchema"
      responses:
          200:
              description: response for 200 code
              schema:
                $ref: "#/definitions/BarBodySchema"
    """
    schema = validation.BarBodySchema(many=True)
    struct = schema.loads(request.body or "{}")
    return struct.data


@view_config(route_name="openapi_spec", renderer="json")
def api_spec(request):
    """
    Serve the spec to explorer
    """
    spec = APISpec(title="Some API", version="1.0.0", plugins=[MarshmallowPlugin()])
    # using marshmallow plugin here
    spec.definition("FooBodySchema", schema=validation.FooBodySchema)
    spec.definition("BarBodySchema", schema=validation.BarBodySchema(many=True))

    # inspect the `foo_route` and generate operations from docstring
    add_pyramid_paths(spec, "users", request=request)

    # inspection supports filtering via pyramid add_view predicate arguments
    add_pyramid_paths(spec, "bar_route", request=request)
    my_spec = spec.to_dict()
    # you can further mutate the spec dict to include things like security definitions
    return my_spec


@exception_view_config(context="marshmallow.ValidationError", renderer="json")
def marshmallow_invalid_data(context, request):
    request.response.status = 422
    return context.messages


def build_wsgi_app():
    with Configurator() as config:
        config.add_route("users", "/users")
        config.add_route("bar_route", "/bar")
        config.add_route("openapi_spec", "/openapi.json")

        config.include("pyramid_apispec.views")
        config.pyramid_apispec_add_explorer(spec_route_name="openapi_spec")
        config.scan(".")
        app = config.make_wsgi_app()
    return app


if __name__ == "__main__":
    app = build_wsgi_app()
    server = make_server("0.0.0.0", 6543, app)
    print("visit api explorer at http://127.0.0.1:6543/api-explorer")
    server.serve_forever()
