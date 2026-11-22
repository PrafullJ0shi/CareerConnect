"""Database helpers for CareerConnect."""

from __future__ import annotations

import os
import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    job_type TEXT NOT NULL,
    description TEXT NOT NULL,
    email TEXT NOT NULL
);
"""

SEED_JOBS = [
    (
        "Junior Python Developer",
        "Nimbus Labs",
        "Dehradun",
        "Full-time",
        "Nimbus Labs is looking for a Junior Python Developer to help build internal tools and small web services. You will write clear Python code, work with SQLite and REST endpoints, and collaborate with a compact product team. This role suits a recent graduate or early-career developer who is comfortable learning on the job and writing well-structured programs.",
        "hiring@nimbuslabs.example",
    ),
    (
        "Frontend Web Intern",
        "Riverstone Digital",
        "Remote",
        "Internship",
        "Riverstone Digital offers a frontend internship for students who want practical experience with HTML, CSS, and accessible interface development. Interns will help implement landing pages, refine layouts for mobile screens, and test forms in modern browsers. Mentorship is provided, and prior academic project work is welcome.",
        "internships@riverstone.example",
    ),
    (
        "Data Analyst",
        "Himalaya Insights",
        "Bengaluru",
        "Full-time",
        "Himalaya Insights is hiring a Data Analyst to turn operational records into clear reports for business teams. The work includes cleaning datasets, writing SQL queries, building dashboards, and explaining findings in plain language. Familiarity with spreadsheets and a programming language such as Python is expected.",
        "careers@himalayainsights.example",
    ),
    (
        "Customer Support Associate",
        "BrightDesk",
        "New Delhi",
        "Part-time",
        "BrightDesk needs a part-time Customer Support Associate to answer product questions and log support tickets. The role requires clear written communication, patience with first-time users, and comfort working through a shared inbox. Shifts are scheduled during weekday afternoons, with training provided in the first week.",
        "people@brightdesk.example",
    ),
    (
        "UX Designer",
        "Northline Studio",
        "Pune",
        "Contract",
        "Northline Studio is seeking a contract UX Designer to improve the flow of a client dashboard. You will review existing screens, prepare wireframes, run lightweight usability checks, and hand off specifications to engineers. A portfolio showing web or mobile product work is required for consideration.",
        "studio@northline.example",
    ),
    (
        "Backend Engineer",
        "Kiteworks",
        "Hyderabad",
        "Full-time",
        "Kiteworks is hiring a Backend Engineer to design and maintain API services used by its web applications. Responsibilities include writing Python services, modelling data, reviewing pull requests, and improving reliability. Experience with Flask or a similar framework, and with relational databases, will help you contribute quickly.",
        "jobs@kiteworks.example",
    ),
    (
        "Marketing Coordinator",
        "Greenleaf Retail",
        "Mumbai",
        "Full-time",
        "Greenleaf Retail is looking for a Marketing Coordinator to support campaign planning and store communications. You will draft copy, schedule posts, track simple performance metrics, and coordinate with store managers. Strong organisation and clear writing are more important than prior agency experience.",
        "talent@greenleaf.example",
    ),
    (
        "QA Tester",
        "Cloudyard",
        "Remote",
        "Contract",
        "Cloudyard needs a contract QA Tester to exercise a browser-based application before each release. You will write test cases, report defects with clear reproduction steps, and verify fixes. Experience testing web forms, search, and responsive layouts is useful, and comfort with issue trackers is expected.",
        "qa@cloudyard.example",
    ),
]


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        db_path = current_app.config["DATABASE"]
        parent = os.path.dirname(db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.executescript(SCHEMA)
    count = db.execute("SELECT COUNT(*) AS n FROM jobs").fetchone()["n"]
    if count == 0:
        db.executemany(
            """
            INSERT INTO jobs (title, company, location, job_type, description, email)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            SEED_JOBS,
        )
        db.commit()


def init_app(app) -> None:
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()


def search_jobs(query: str | None = None) -> list[sqlite3.Row]:
    db = get_db()
    if query:
        pattern = f"%{query}%"
        return db.execute(
            """
            SELECT id, title, company, location, job_type, description, email
            FROM jobs
            WHERE title LIKE ?
               OR company LIKE ?
               OR location LIKE ?
               OR job_type LIKE ?
            ORDER BY id DESC
            """,
            (pattern, pattern, pattern, pattern),
        ).fetchall()
    return db.execute(
        """
        SELECT id, title, company, location, job_type, description, email
        FROM jobs
        ORDER BY id DESC
        """
    ).fetchall()


def get_job(job_id: int) -> sqlite3.Row | None:
    return get_db().execute(
        """
        SELECT id, title, company, location, job_type, description, email
        FROM jobs
        WHERE id = ?
        """,
        (job_id,),
    ).fetchone()


def add_job(
    title: str,
    company: str,
    location: str,
    job_type: str,
    description: str,
    email: str,
) -> int:
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO jobs (title, company, location, job_type, description, email)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, company, location, job_type, description, email),
    )
    db.commit()
    return int(cursor.lastrowid)
