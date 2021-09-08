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

Or visit [generated documentation here](https://ergo.github.io/pyramid_apispec/gh-pages)
for an example of the demo site.
(please note that actual REST API is not working in GitHub pages)

**Note:** The demo site is using OpenAPI/Swagger v2.0.
OpenAPI 3.0 is supported as well, it just uses a different YAML schema so pay attention to examples online.

# Example

This example is based on [apispec](https://apispec.readthedocs.io/en/latest/#example-application),
adapted for Pyramid and `pyramid_apispec` (updated as of `apispec` v5.1.0).

*This example is using OpenAPI 3.0.2*

## Hinting a route and its view:

Add the OpenAPI YAML to the view docstring.
Optionally use Marshmallow schemas to define the inputs and outputs.

```python
import uuid

from marshmallow import Schema, fields
from pyramid.view import view_config

# Optional marshmallow support
class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    
class PetSchema(Schema):
    categories = fields.List(fields.Nested(CategorySchema))
    name = fields.Str()

@view_config(route_name="random_pet", renderer="json")
def random_pet(request):
    """A cute furry animal endpoint.
    ---
    get:
      description: Get a random pet
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: PetSchema
    """
    # Hardcoded example data
    pet_data = {
        "name": "sample_pet_" + str(uuid.uuid1()),
        "categories": [{"id": 1, "name": "sample_category"}],
    }
    return PetSchema().dump(pet_data)
```

For more details on how to document the API, see the [OpenAPI specification](https://swagger.io/specification/).

## Rendering the spec as JSON response:

```python
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from pyramid.view import view_config
from pyramid_apispec.helpers import add_pyramid_paths

@view_config(route_name="openapi_spec", renderer="json")
def api_spec(request):
    """View to generate the OpenAPI JSON output."""
    spec = APISpec(
        title="Some API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin()],
    )

    # Optional security scheme support
    api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
    spec.components.security_scheme("ApiKeyAuth", api_key_scheme)
    
    # Optionally register Marshmallow schema for more flexibility
    spec.components.schema("Pet", schema=PetSchema)
    
    # inspect the `random_pet` route and generate operations from docstring
    add_pyramid_paths(spec, 'random_pet', request=request)

    return spec.to_dict()
```

## Adding the API Explorer View

To complement the specification file generation, this package can also provide an API explorer
for your application's API via the Swagger UI project:

```python
config.include("pyramid_apispec.views")
config.add_route("openapi_spec", "/openapi.json")
config.pyramid_apispec_add_explorer(spec_route_name="openapi_spec")
```

By default you need to pass the route name of the view that serves the OpenAPI
specification in your application. If needed you can specify a Pyramid `permission` or
custom callable (`script_generator` argument) to override the default JavaScript
configuration of Swagger UI.

The default URL for the explorer is `/api-explorer`. This setting is controlled
via the `explorer_route_path` argument - the route is registered as `pyramid_apispec.api_explorer_path`.

# Running tests

    pip install -e '.[dev]'
    tox
