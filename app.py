
from flask import Flask, render_template, Response, request

from weasyprint import HTML, default_url_fetcher

app = Flask(__name__)


def url_fetcher(url):
    """
    :type url: str
    """
    if url.startswith("file:///static/"):
        url = url.replace("file:///static/", "file://%s/" % get_base_url())

    return default_url_fetcher(url)


def get_base_url():
    import os.path

    return os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))


def create_doc(**kwargs):
    return HTML(url_fetcher=url_fetcher, base_url=get_base_url(), **kwargs)


@app.route("/", methods=["GET"])
def home():
    return Response(render_template("intro.html"))


@app.route('/render/<template_name>', methods=["GET"])
def render_page(template_name):
    try:
        rendered_template = render_template("pdf/%s.html" % template_name)
    except:
        return "There is no page dude, turn back!", 404

    if "html" in request.args:
        return Response(rendered_template)

    doc = create_doc(string=rendered_template).render()

    return Response(doc.write_pdf(), mimetype="application/pdf")


if __name__ == '__main__':
    app.run(debug=True, port=8080)
