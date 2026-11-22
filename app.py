"""CareerConnect Flask application."""

from __future__ import annotations

import os
import re

from flask import Flask, flash, redirect, render_template, request, url_for

from db import add_job, get_job, init_app, search_jobs

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
REQUIRED_FIELDS = ("title", "company", "location", "job_type", "description", "email")
JOB_TYPES = ("Full-time", "Part-time", "Contract", "Internship")


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    default_db = os.path.join(app.instance_path, "careerconnect.db")
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-insecure-secret-key"),
        DATABASE=os.environ.get("DATABASE", default_db),
        DEBUG=False,
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    db_parent = os.path.dirname(app.config["DATABASE"])
    if db_parent:
        os.makedirs(db_parent, exist_ok=True)

    init_app(app)

    @app.route("/")
    def home():
        q = request.args.get("q", "").strip()
        jobs = search_jobs(q or None)
        return render_template("index.html", jobs=jobs, q=q)

    @app.route("/job/<int:job_id>")
    def job_detail(job_id: int):
        job = get_job(job_id)
        if job is None:
            return render_template("404.html"), 404
        return render_template("job.html", job=job)

    @app.route("/post", methods=["GET", "POST"])
    def post_job():
        errors: list[str] = []
        form = {field: "" for field in REQUIRED_FIELDS}
        if request.method == "POST":
            form = {field: request.form.get(field, "").strip() for field in REQUIRED_FIELDS}
            missing = [field for field in REQUIRED_FIELDS if not form[field]]
            if missing:
                errors.append("Please fill in all required fields.")
            if form["email"] and not EMAIL_RE.fullmatch(form["email"]):
                errors.append("Please enter a valid email address.")
            if not errors:
                add_job(
                    title=form["title"],
                    company=form["company"],
                    location=form["location"],
                    job_type=form["job_type"],
                    description=form["description"],
                    email=form["email"],
                )
                flash("Your job listing has been posted successfully.", "success")
                return redirect(url_for("home"))
        return render_template("post.html", form=form, errors=errors, job_types=JOB_TYPES)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=False)
