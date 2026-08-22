import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template

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
