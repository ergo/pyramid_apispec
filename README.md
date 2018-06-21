# pyramid_apispec

pyramid_apispec allows you to create an OpenAPI specification file and an online 
OpenAPI explorer using the Swagger UI project for your Pyramid application 
and its Marshmallow schemas. 

* Pyramid - http://trypyramid.com
* Marshmallow - http://marshmallow.readthedocs.io/en/latest/
* ApiSpec - http://apispec.readthedocs.io/en/latest/
* Swagger UI - https://swagger.io/tools/swagger-ui/

# Installation

    pip install pyramid_apispec

# Basic usage

Check out the demo folder and minimal application example by running:

    pip install -e[demo]
    python demo/app.py
    

Hinting a route and its view:

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
                        $ref: #/definitions/BarBodySchema
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

# Adding api explorer view

To compliment the spec generation this package can also provide explorer
for your application API via Swagger UI project:

    config.include('pyramid_apispec.views')
    config.pyramid_apispec_add_explorer(
        spec_route_name='openapi_spec')

By default you need to pass the route name of the view that serves the open api 
spec in your application, if needed you can specify pyramid `permission` or 
custom callable (`script_generator` argument) to override default javascript 
config of Swagger UI.

The default url for the explorer is `/api-explorer`, this setting is controlled
via `explorer_route_path` argument, 

# Running tests

    pip install -e .[dev]
    tox
