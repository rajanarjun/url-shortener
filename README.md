# URL Shortener

A simple URL shortener web application that takes a long URL and generates a short, shareable link, just like TinyURL and Bitly.

## Features
- Accepts a long URL and generates a unique short URL
- Redirects users to the original long URL
- Simple web interface built with HTML templates
- Lightweight and easy to deploy

## Progress
- **Switching to Flask** — Refactoring the existing FastAPI implementation to Flask.
- **Improved Encoding** — More standardized and reliable short-link generation method, possibly using UUIDs or hash-based encoding.
- **Multiple Client Support** — Support for multiple users or clients, user-specific short URLs.
- **Deployment Setup** — Method Undecided.

## Tech Stack
**Flask Branch**
- Python 3.12
- Web Framework: Flask
- Templating: HTML/CSS
- Database: PostgreSQL

**FastAPI Branch**
- Python 3.12
- Web Framework: FastAPI
- Templating: Jinja2
- Database: PostgreSQL

## License
MIT License — see `LICENSE` file.

