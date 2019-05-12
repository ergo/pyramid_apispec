import importlib
from string import Template

import pkg_resources
from pyramid.response import Response

from pyramid_apispec.exceptions import PyramidApiSpecException


def includeme(config):
    settings = config.registry.settings
    config.add_directive(
        "pyramid_apispec_add_explorer", "pyramid_apispec.views:build_api_explorer_view"
    )


def build_api_explorer_view(
    config,
    explorer_route_path="/api-explorer",
    spec_route_name=None,
    script_generator="pyramid_apispec.views:swagger_ui_script_template",
    permission=None,
    route_args=None,
    view_args=None,
    **kwargs
):
    """
        Create view that will serve template for swagger UI with proper
        urls substituted

    :param config:
    :param explorer_route_path:
    :param spec_route_name:
    :param script_generator:
    :param permission:
    :param route_args:
    :param view_args:
    :param kwargs:
    :return:
    """
    route_args = route_args or {}
    view_args = view_args or {}
    view_args["permission"] = permission
    config.add_route(
        "pyramid_apispec.api_explorer_path", explorer_route_path, **route_args
    )
    template = pkg_resources.resource_string(
        "pyramid_apispec", "static/index.html"
    ).decode("utf8")
    package, callable = script_generator.split(":")
    imported_package = importlib.import_module(package)

    def swagger_ui_template_view(request):
        if not spec_route_name:
            raise PyramidApiSpecException(
                "spec_route_name argument needs to be present"
            )

        script_callable = getattr(imported_package, callable)
        version = kwargs.get("ui_version", "3.17.1")
        html = Template(template).safe_substitute(
            swagger_ui_script=script_callable(request, spec_route_name, **kwargs),
            version=version,
        )
        return Response(html)

    config.add_view(
        swagger_ui_template_view,
        route_name="pyramid_apispec.api_explorer_path",
        **view_args
    )


def swagger_ui_script_template(request, spec_route_name, **kwargs):
    """
    Generates the <script> code that bootstraps Swagger UI, it will be injected
    into index template

    :param request:
    :param spec_route_name:
    :return:
    """
    template = pkg_resources.resource_string(
        "pyramid_apispec", "static/index_script_template.html"
    ).decode("utf8")
    return Template(template).safe_substitute(
        swagger_spec_url=request.route_url(spec_route_name)
    )
