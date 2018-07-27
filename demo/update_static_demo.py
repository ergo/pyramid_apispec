import io
import json

from webtest import TestApp
from app import build_wsgi_app

app = TestApp(build_wsgi_app())

explorer_html = app.get("/api-explorer").text
spec_json = app.get("/openapi.json").json

explorer_html = explorer_html.replace("http://localhost/", "")


with io.open("../gh-pages/index.html", "w") as f:
    f.write(explorer_html)

with io.open("../gh-pages/openapi.json", "w") as f:
    f.write(json.dumps(spec_json, indent=4))
