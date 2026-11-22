(function () {
  "use strict";

  var STORAGE_KEY = "careerconnect-jobs";
  var FLASH_KEY = "careerconnect-flash";
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  var SEED_JOBS = [
    {
      id: 1,
      title: "Junior Python Developer",
      company: "Nimbus Labs",
      location: "Dehradun",
      job_type: "Full-time",
      description:
        "Nimbus Labs is looking for a Junior Python Developer to help build internal tools and small web services. You will write clear Python code, work with SQLite and REST endpoints, and collaborate with a compact product team. This role suits a recent graduate or early-career developer who is comfortable learning on the job and writing well-structured programs.",
      email: "hiring@nimbuslabs.example",
    },
    {
      id: 2,
      title: "Frontend Web Intern",
      company: "Riverstone Digital",
      location: "Remote",
      job_type: "Internship",
      description:
        "Riverstone Digital offers a frontend internship for students who want practical experience with HTML, CSS, and accessible interface development. Interns will help implement landing pages, refine layouts for mobile screens, and test forms in modern browsers. Mentorship is provided, and prior academic project work is welcome.",
      email: "internships@riverstone.example",
    },
    {
      id: 3,
      title: "Data Analyst",
      company: "Himalaya Insights",
      location: "Bengaluru",
      job_type: "Full-time",
      description:
        "Himalaya Insights is hiring a Data Analyst to turn operational records into clear reports for business teams. The work includes cleaning datasets, writing SQL queries, building dashboards, and explaining findings in plain language. Familiarity with spreadsheets and a programming language such as Python is expected.",
      email: "careers@himalayainsights.example",
    },
    {
      id: 4,
      title: "Customer Support Associate",
      company: "BrightDesk",
      location: "New Delhi",
      job_type: "Part-time",
      description:
        "BrightDesk needs a part-time Customer Support Associate to answer product questions and log support tickets. The role requires clear written communication, patience with first-time users, and comfort working through a shared inbox. Shifts are scheduled during weekday afternoons, with training provided in the first week.",
      email: "people@brightdesk.example",
    },
    {
      id: 5,
      title: "UX Designer",
      company: "Northline Studio",
      location: "Pune",
      job_type: "Contract",
      description:
        "Northline Studio is seeking a contract UX Designer to improve the flow of a client dashboard. You will review existing screens, prepare wireframes, run lightweight usability checks, and hand off specifications to engineers. A portfolio showing web or mobile product work is required for consideration.",
      email: "studio@northline.example",
    },
    {
      id: 6,
      title: "Backend Engineer",
      company: "Kiteworks",
      location: "Hyderabad",
      job_type: "Full-time",
      description:
        "Kiteworks is hiring a Backend Engineer to design and maintain API services used by its web applications. Responsibilities include writing Python services, modelling data, reviewing pull requests, and improving reliability. Experience with Flask or a similar framework, and with relational databases, will help you contribute quickly.",
      email: "jobs@kiteworks.example",
    },
    {
      id: 7,
      title: "Marketing Coordinator",
      company: "Greenleaf Retail",
      location: "Mumbai",
      job_type: "Full-time",
      description:
        "Greenleaf Retail is looking for a Marketing Coordinator to support campaign planning and store communications. You will draft copy, schedule posts, track simple performance metrics, and coordinate with store managers. Strong organisation and clear writing are more important than prior agency experience.",
      email: "talent@greenleaf.example",
    },
    {
      id: 8,
      title: "QA Tester",
      company: "Cloudyard",
      location: "Remote",
      job_type: "Contract",
      description:
        "Cloudyard needs a contract QA Tester to exercise a browser-based application before each release. You will write test cases, report defects with clear reproduction steps, and verify fixes. Experience testing web forms, search, and responsive layouts is useful, and comfort with issue trackers is expected.",
      email: "qa@cloudyard.example",
    },
  ];

  function loadJobs() {
    try {
      var stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored) {
        var parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length) {
          return parsed;
        }
      }
    } catch (err) {
      /* ignore storage errors and fall back to seed data */
    }
    return SEED_JOBS.slice();
  }

  function saveJobs(jobs) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(jobs));
    } catch (err) {
      /* storage may be unavailable */
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function excerpt(text) {
    return text.length > 170 ? text.slice(0, 170) + "…" : text;
  }

  function searchJobs(jobs, query) {
    if (!query) {
      return jobs.slice().sort(function (a, b) { return b.id - a.id; });
    }
    var needle = query.toLowerCase();
    return jobs
      .filter(function (job) {
        return [job.title, job.company, job.location, job.job_type]
          .join(" ")
          .toLowerCase()
          .indexOf(needle) !== -1;
      })
      .sort(function (a, b) { return b.id - a.id; });
  }

  function renderList(jobs, query) {
    var heading = document.getElementById("list-heading");
    var count = document.getElementById("list-count");
    var list = document.getElementById("job-list");
    if (!list) return;

    heading.textContent = query ? "Search results" : "Open roles";
    count.textContent = query
      ? jobs.length + " result" + (jobs.length !== 1 ? "s" : "") + " for “" + query + "”"
      : jobs.length + " listing" + (jobs.length !== 1 ? "s" : "");

    if (!jobs.length) {
      list.innerHTML =
        '<div class="empty"><h2>No jobs matched your search</h2>' +
        '<p>Try a different keyword, or <a href="index.html">browse all openings</a>.</p></div>';
      return;
    }

    list.innerHTML =
      '<div class="job-grid">' +
      jobs
        .map(function (job) {
          return (
            '<a class="job-card" href="job.html?id=' +
            encodeURIComponent(job.id) +
            '">' +
            '<span class="chip">' +
            escapeHtml(job.job_type) +
            "</span>" +
            "<h2>" +
            escapeHtml(job.title) +
            "</h2>" +
            '<p class="company">' +
            escapeHtml(job.company) +
            "</p>" +
            '<div class="meta"><span class="chip gold">' +
            escapeHtml(job.location) +
            "</span></div>" +
            '<p class="excerpt">' +
            escapeHtml(excerpt(job.description)) +
            "</p>" +
            '<span class="card-link">View details →</span></a>'
          );
        })
        .join("") +
      "</div>";
  }

  function renderNotFound(container) {
    document.title = "Page not found · CareerConnect";
    container.innerHTML =
      '<section class="wrap not-found">' +
      '<p class="kicker">404</p>' +
      "<h1>This job listing could not be found</h1>" +
      '<p class="lede" style="margin-inline:auto;">The page or vacancy you requested is not available. It may have been removed, or the link may be incorrect.</p>' +
      '<p style="margin-top:1.4rem;"><a class="btn btn-dark" href="index.html">Back to job listings</a></p>' +
      "</section>";
  }

  function renderJob(job, container) {
    document.title = job.title + " · " + job.company + " · CareerConnect";
    var mail = "mailto:" + String(job.email);
    var apply = mail + "?subject=" + encodeURIComponent("Application: " + job.title);
    container.innerHTML =
      '<section class="wrap page-head job-hero">' +
      '<p class="kicker">Job details</p>' +
      "<h1>" +
      escapeHtml(job.title) +
      "</h1>" +
      '<p class="lede">' +
      escapeHtml(job.company) +
      "</p>" +
      '<div class="meta"><span class="chip">' +
      escapeHtml(job.job_type) +
      '</span><span class="chip gold">' +
      escapeHtml(job.location) +
      "</span></div></section>" +
      '<section class="wrap job-layout"><article class="panel job-body"><h2>About this role</h2><p>' +
      escapeHtml(job.description) +
      '</p></article><aside class="panel"><p class="contact-label">Contact the employer</p>' +
      '<a class="email-link" href="' +
      mail +
      '">' +
      escapeHtml(job.email) +
      "</a>" +
      '<p style="color:var(--ink-soft);font-size:0.92rem;margin:0 0 1rem;">This opens your email application with the address supplied on the listing.</p>' +
      '<a class="btn btn-primary" href="' +
      apply +
      '">Email employer</a></aside></section>';
  }

  function showFlash() {
    var slot = document.getElementById("flash-slot");
    if (!slot) return;
    try {
      var message = window.sessionStorage.getItem(FLASH_KEY);
      if (message) {
        slot.hidden = false;
        slot.innerHTML = '<p class="flash flash-success" role="status">' + escapeHtml(message) + "</p>";
        window.sessionStorage.removeItem(FLASH_KEY);
      }
    } catch (err) {
      /* ignore */
    }
  }

  var page = document.body;
  var path = window.location.pathname.split("/").pop() || "index.html";
  var jobs = loadJobs();

  if (path === "index.html" || path === "" || path === "CareerConnect") {
    showFlash();
    var params = new URLSearchParams(window.location.search);
    var query = (params.get("q") || "").trim();
    var input = document.getElementById("q");
    if (input) input.value = query;
    renderList(searchJobs(jobs, query), query);
    var form = document.getElementById("search-form");
    if (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var value = (document.getElementById("q").value || "").trim();
        var next = value ? "index.html?q=" + encodeURIComponent(value) : "index.html";
        window.location.href = next;
      });
    }
  } else if (path === "job.html") {
    var id = Number(new URLSearchParams(window.location.search).get("id"));
    var container = document.getElementById("job-page");
    var match = jobs.filter(function (job) { return job.id === id; })[0];
    if (!match) {
      renderNotFound(container);
    } else {
      renderJob(match, container);
    }
  } else if (path === "post.html") {
    var postForm = document.getElementById("post-form");
    postForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var fields = ["title", "company", "location", "job_type", "description", "email"];
      var data = {};
      fields.forEach(function (name) {
        data[name] = (postForm.elements[name].value || "").trim();
      });
      var errors = [];
      if (fields.some(function (name) { return !data[name]; })) {
        errors.push("Please fill in all required fields.");
      }
      if (data.email && !EMAIL_RE.test(data.email)) {
        errors.push("Please enter a valid email address.");
      }
      var box = document.getElementById("form-errors");
      if (errors.length) {
        box.hidden = false;
        box.innerHTML = errors.map(function (err) { return "<p>" + escapeHtml(err) + "</p>"; }).join("");
        return;
      }
      var nextId = jobs.reduce(function (max, job) { return job.id > max ? job.id : max; }, 0) + 1;
      data.id = nextId;
      jobs.push(data);
      saveJobs(jobs);
      try {
        window.sessionStorage.setItem(FLASH_KEY, "Your job listing has been posted successfully.");
      } catch (err) {
        /* ignore */
      }
      window.location.href = "index.html";
    });
  } else if (path === "404.html") {
    /* already rendered */
  }
})();
