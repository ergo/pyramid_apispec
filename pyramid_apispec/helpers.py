"""Pyramid helper. Includes a path helper that allows you to pass a route name
for inspection. Inspects URL rules and view docstrings.

Inspecting a route and its view::

    from pyramid_apispec.helpers import add_pyramid_paths

    @view_config(route_name='foo_route', renderer='json')
    def foo_view():
        \"""A greeting endpoint.

        ---
        x-extension: value
        get:
            description: get a greeting
            responses:
                200:
                    description: a pet to be returned
                    schema: SomeFooBody
        \"""
        return 'hi'

    @view_config(route_name='openapi_spec', renderer='json')
    def api_spec(request):
        spec = APISpec(
            title='Some API',
            version='1.0.0',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        )
        # using marshmallow plugin here
        spec.definition('SomeFooBody', schema=MarshmallowSomeFooBodySchema)

        # inspect the `foo_route` and generate operations from docstring
        add_pyramid_paths(spec, 'foo_route', request=request)

        # inspection supports filtering via pyramid add_view predicate arguments
        add_pyramid_paths(
            spec, 'bar_route', request=request, request_method='post')
        return spec.to_dict()


"""
from apispec.yaml_utils import load_operations_from_docstring, load_yaml_from_docstring
from pyramid.predicates import MatchParamPredicate
from pyramid.threadlocal import get_current_request


def is_string(val):
    return isinstance(val, str)


ALL_METHODS = ("get", "post", "put", "patch", "delete", "head", "options")


def clean_part(part):
    # cleanup regex from route params
    if part.startswith("{") and part.endswith("}") and ":" in part:
        part = part.split(":")[0] + "}"
    return part


def reformat_pattern(pattern):
    if not pattern.startswith("/"):
        pattern = "/%s" % pattern
    parts = pattern.split("/")
    return "/".join([clean_part(p) for p in parts])


def add_pyramid_paths(
    spec,
    route_name,
    request=None,
    request_method=None,
    operations=None,
    autodoc=True,
    **kwargs
):
    """

    Adds a route and view info to spec

    :param spec:
        ApiSpec object
    :param route_name:
        Route name to inspect
    :param request:
        Request object, if `None` then `get_current_request()` will be used
    :param request_method:
        Request method predicate
    :param operations:
        Operations dict that will be used instead of introspection
    :param autodoc:
        Include information about endpoints without markdown docstring
    :param kwargs:
        Additional kwargs for predicate matching
    :return:

    """
    if request is None:
        request = get_current_request()

    registry = request.registry
    introspector = registry.introspector
    route = introspector.get("routes", route_name)
    introspectables = introspector.related(route)
    ignored_view_names = kwargs.pop("ignored_view_names", None)
    # needs to be rewritten to internal name
    if request_method:
        kwargs["request_methods"] = request_method

    for maybe_view in introspectables:
        # skip excluded views/non-views
        if (
            not is_view(maybe_view)
            or not check_methods_matching(maybe_view, **kwargs)
            or should_ignore_view(maybe_view, ignored_views=ignored_view_names)
        ):
            continue

        pattern = route["pattern"]
        pattern = reformat_pattern(pattern)
        if maybe_view.get("match_param"):
            # replace route patterns that are specified in the view's match_param argument,
            # so that route URLs are unique and accurate
            match_params = MatchParamPredicate(maybe_view["match_param"], None)
            for key, value in match_params.reqs:
                pattern = pattern.replace("{%s}" % key, value)
        spec.path(
            pattern, operations=get_operations(maybe_view, operations, autodoc=autodoc)
        )


def is_view(introspectable):
    return introspectable.category_name == "views"


def should_ignore_view(introspectable, **kwargs):
    to_ignore = kwargs.get("ignored_view_names")
    if to_ignore is None:
        to_ignore = ["cornice.pyramidhook._fallback_view"]

    for name in to_ignore:
        if name in introspectable.title:
            return True
    return False


def check_methods_matching(view, **kwargs):
    for kw in kwargs.keys():
        # request_methods can be either a list of strings or a string
        # so lets normalize via sets
        if kw == "request_methods":
            if is_string(kwargs[kw]):
                kwargs[kw] = [kwargs[kw]]
            methods = view.get(kw) or ALL_METHODS
            if is_string(methods):
                methods = [methods]
            if not set(kwargs[kw] or []).intersection(methods):
                return False
        else:
            if not view.get(kw) == kwargs[kw]:
                return False
    return True


def get_operations(view, operations, autodoc=True):
    if operations is not None:
        return operations

    operations = {}

    # views can be class based
    if view.get("attr"):
        global_meta = load_operations_from_docstring(view["callable"].__doc__)
        if global_meta:
            operations.update(global_meta)
        f_view = getattr(view["callable"], view["attr"])
    # or just function callables
    else:
        f_view = view.get("callable")

    methods = view.get("request_methods")
    view_operations = load_operations_from_docstring(f_view.__doc__)
    if not view_operations:
        view_operations = {}
        if is_string(methods):
            methods = [methods]
        if not methods:
            methods = ALL_METHODS[:]
        operation = load_yaml_from_docstring(f_view.__doc__)
        if operation:
            for method in methods:
                view_operations[method.lower()] = operation
        elif autodoc:
            for method in methods:
                view_operations.setdefault(method.lower(), {"responses": {}})
    operations.update(view_operations)

    return operations
