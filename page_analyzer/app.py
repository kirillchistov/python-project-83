import os
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from requests.exceptions import RequestException

from .db import (
    create_check,
    create_url,
    find_url_by_id,
    find_url_by_name,
    get_checks,
    get_urls,
)
from .http import get_url_status_code
from .url_utils import is_valid_url, normalize_url

load_dotenv()

APP_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    template_folder=str(APP_DIR / "templates"),
    static_folder=str(APP_DIR / "static"),
)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/urls")
def urls_create():
    raw_url = request.form.get("url", "").strip()
    if not is_valid_url(raw_url):
        flash("Некорректный URL", "danger")
        return render_template("index.html", url=raw_url), 422

    name = normalize_url(raw_url)
    existing = find_url_by_name(name)
    if existing:
        flash("Страница уже существует", "info")
        return redirect(url_for("url_show", id=existing["id"]))

    url_id = create_url(name)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("url_show", id=url_id))


@app.get("/urls")
def urls():
    return render_template("urls.html", urls=get_urls())


@app.get("/urls/<int:id>")
def url_show(id):
    url = find_url_by_id(id)
    if url is None:
        abort(404)
    checks = get_checks(id)
    return render_template("url.html", url=url, checks=checks)


@app.post("/urls/<int:id>/checks")
def url_checks(id):
    url = find_url_by_id(id)
    if url is None:
        abort(404)
    try:
        status_code = get_url_status_code(url["name"])
    except RequestException:
        flash("Произошла ошибка при проверке", "danger")
    else:
        create_check(id, status_code)
        flash("Страница успешно проверена", "success")
    return redirect(url_for("url_show", id=id))
