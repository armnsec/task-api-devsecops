# DevSecOps Pipeline: Automated Container Security Scanning

A small Flask REST API (Task Manager microservice) used as the target
application for a fully automated **Secure SDLC / DevSecOps CI/CD pipeline**
built with GitHub Actions, Docker, and open-source security tooling.

## Why this project

Modern Application Security teams don't just review code manually — they
build automated tooling into the CI/CD pipeline so vulnerabilities are
caught **before** they reach production. This project demonstrates that
workflow end-to-end.

## Architecture

```
Push / PR → Unit Tests → SAST (Bandit) ─┐
                        → Container Build → Image Scan (Trivy) ─┴→ Push to Registry (main only)
```

## Tech Stack

- **App:** Python 3.12, Flask (simple in-memory Task Manager REST API)
- **Containerization:** Docker (non-root user, minimal slim base image)
- **CI/CD:** GitHub Actions
- **SAST:** [Bandit](https://bandit.readthedocs.io/) — scans Python source for common security issues (hardcoded secrets, unsafe functions, etc.)
- **Container / Dependency Scanning:** [Trivy](https://aquasecurity.github.io/trivy/) — scans the built Docker image for known CVEs in OS packages and Python dependencies
- **Registry:** GitHub Container Registry (GHCR)

## Security Controls Implemented

| Control | Where |
|---|---|
| Non-root container user | `Dockerfile` |
| Minimal base image (`python:3.12-slim`) to reduce attack surface | `Dockerfile` |
| Automated SAST on every push/PR | `security-pipeline.yml` |
| Automated container CVE scanning, pipeline fails on HIGH/CRITICAL | `security-pipeline.yml` |
| Input validation on API payloads | `app.py` |
| Debug mode disabled in Flask | `app.py` |
| Security gate: image is only pushed to registry after passing all scans | `security-pipeline.yml` |

## Running Locally

```bash
# Build and run with Docker
docker build -t task-api .
docker run -p 5000:5000 task-api

# Or run locally with Python
pip install -r requirements.txt
python app.py
```

## Running Tests & Scans Locally

```bash
# Unit tests
pip install pytest && pytest -v

# SAST scan
pip install bandit
bandit -r . -x ./test_app.py

# Container vulnerability scan (requires Trivy installed)
docker build -t task-api .
trivy image task-api
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task (`{"title": "..."}`) |
| GET | `/tasks/<id>` | Get a single task |
| PUT | `/tasks/<id>/complete` | Mark task as done |
| DELETE | `/tasks/<id>` | Delete a task |

## Next Steps / Roadmap

- Add Kubernetes deployment manifests + `kube-bench` / `Trivy k8s` cluster scanning
- Add DAST scanning (OWASP ZAP baseline scan) against the running container in CI
- Add Semgrep for deeper SAST rule coverage
