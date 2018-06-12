# pyramid_apispec

ApiSpec Pyramid plugin for API generation. This package contains helper
code for quick documentation of pyramid REST API's with 
openapi (swagger) specification.


# Installation

    pip install pyramid_apispec

# Basic usage

Hinting a route and its view:

    @view_config(route_name='foo_route', renderer='json')
    def foo_view():
        """A greeting endpoint.

        ---
        x-extension: value
        get:
            description: get a greeting
            responses:
                200:
                    description: a pet to be returned
                    schema:
                        $ref: #/definitions/SomeFooBody
        """
        return 'hi'

Rendering the spec as JSON response:

    from pyramid_apispec.helpers import add_pyramid_paths

    @view_config(route_name='openapi_spec', renderer='json')
    def api_spec(request):
        spec = APISpec(
            title='Some API',
            version='1.0.0',
            plugins=[
                'apispec.ext.marshmallow'
            ],
        )
        # using marshmallow plugin here
        spec.definition('SomeFooBody', schema=MarshmallowSomeFooBodySchema)

        # inspect the `foo_route` and generate operations from docstring
        add_pyramid_paths(spec, 'foo_route', request=request)

        # inspection supports filtering via pyramid add_view predicate arguments
        add_pyramid_paths(
            spec, 'bar_route', request=request, request_method='post')
        return spec.to_dict()


# Running tests

    pip install -e .[dev]
    tox
