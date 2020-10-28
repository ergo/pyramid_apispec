# pyramid_apispec

pyramid_apispec allows you to create an [OpenAPI specification file](https://swagger.io/specification/)
using [apispec](http://apispec.readthedocs.io/en/latest/) and an online OpenAPI explorer using the
[Swagger UI](https://swagger.io/tools/swagger-ui/) project for your [Pyramid](https://trypyramid.com)
application and its [marshmallow](https://marshmallow.readthedocs.io/en/latest/) schemas.

# Installation

    pip install pyramid_apispec

# Basic usage

Check out the demo folder and minimal application example by running:

    pip install -e '.[demo]'
    python demo/app.py

You can then visit your API explorer page at http://0.0.0.0:6543/api-explorer.

# Examples

Visit [generated documentation here](https://ergo.github.io/pyramid_apispec/gh-pages)
(please note that actual REST API is not working in github pages)

**Note:** This example is specific to OpenAPI/Swagger v2.x.
OpenAPI 3.x.x is supported as well, it just uses a different YAML schema so pay attention to examples online
(for example, the [apispec examples](https://apispec.readthedocs.io/en/latest/using_plugins.html#example-flask-and-marshmallow-plugins)
use v3).

## Hinting a route and its view:

    @view_config(route_name='foo_route', renderer='json')
    def foo_view():
        """A greeting endpoint.

        ---
        x-extension: value
        get:
            description: some description
            responses:
                200:
                    description: response for 200 code
                    schema:
                        $ref: "#/definitions/BarBodySchema"
        """
        return 'hi'

## Rendering the spec as JSON response:

    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from pyramid_apispec.helpers import add_pyramid_paths

    @view_config(route_name='openapi_spec', renderer='json')
    def api_spec(request):
        spec = APISpec(
            title='Some API',
            version='1.0.0',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        )
        # using marshmallow plugin here
        spec.components.schema('SomeFooBody', schema=MarshmallowSomeFooBodySchema)

        # inspect the `foo_route` and generate operations from docstring
        add_pyramid_paths(spec, 'foo_route', request=request)

        # inspection supports filtering via pyramid add_view predicate arguments
        add_pyramid_paths(
            spec, 'bar_route', request=request, request_method='post')
        return spec.to_dict()

# Adding the API explorer view

To complement the specification file generation, this package can also provide an API explorer
for your application's API via the Swagger UI project:

    config.include('pyramid_apispec.views')
    config.add_route("openapi_spec", "/openapi.json")
    config.pyramid_apispec_add_explorer(
        spec_route_name='openapi_spec')

By default you need to pass the route name of the view that serves the OpenAPI
specification in your application. If needed you can specify a Pyramid `permission` or
custom callable (`script_generator` argument) to override the default JavaScript
configuration of Swagger UI.

The default URL for the explorer is `/api-explorer`. This setting is controlled
via the `explorer_route_path` argument - the route is registered as `pyramid_apispec.api_explorer_path`.

# Running tests

    pip install -e '.[dev]'
    tox
