from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from overflow.optimizer import optimize_text
from overflow.pipeline import process_text
from overflow.policy import validate_policy
from overflow.privacy import redact_text
from overflow.providers import PROVIDER_NAMES
from overflow.security import scan_text

app = FastAPI(
    title="Overflow Gateway",
    description="AI governance and optimization middleware",
    version="0.2.0"
)


class TextRequest(BaseModel):
    text: str


class ChatRequest(BaseModel):
    text: str
    policy: dict = None
    optimize: bool = True
    provider: str = "mock"


class PolicyRequest(BaseModel):
    policy: dict


def _dashboard_html():
    candidates = [
        Path(__file__).resolve().parents[3] / "ui" / "index.html",
        Path.cwd() / "ui" / "index.html"
    ]
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8")
    return "<h1>Overflow</h1><p>Dashboard not found.</p>"


@app.get("/")
def root():
    return {
        "name": "Overflow Gateway",
        "status": "running",
        "docs": "/docs",
        "dashboard": "/dashboard"
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return _dashboard_html()


@app.get("/v1/health")
def health():
    return {"status": "ok"}


@app.get("/v1/providers")
def providers():
    return {"providers": PROVIDER_NAMES}


@app.post("/v1/check")
def check(req: TextRequest):
    report = redact_text(req.text)
    return {"redacted": report.output, "counts": report.counts}


@app.post("/v1/security")
def security(req: TextRequest):
    report = scan_text(req.text)
    return {
        "allowed": report.allowed,
        "reasons": report.reasons,
        "counts": report.counts
    }


@app.post("/v1/policy/validate")
def policy_validate(req: PolicyRequest):
    errors = validate_policy(req.policy)
    if errors:
        return {"valid": False, "errors": errors}
    return {"valid": True}


@app.post("/v1/chat")
def chat(req: ChatRequest):
    result = process_text(
        req.text,
        policy=req.policy,
        optimize=req.optimize,
        provider_name=req.provider,
        audit_enabled=False
    )

    if not result.allowed:
        return {
            "allowed": False,
            "reasons": result.reasons,
            "privacy_counts": result.privacy_counts,
            "security_counts": result.security_counts
        }

    return {
        "allowed": True,
        "output_text": result.output_text,
        "response_text": result.response_text,
        "privacy_counts": result.privacy_counts,
        "security_counts": result.security_counts,
        "optimization": result.optimization,
        "provider": result.provider
    }


@app.post("/v1/optimize")
def optimize(req: TextRequest):
    report = optimize_text(req.text)
    return {
        "output": report.output,
        "original_tokens": report.original_tokens,
        "optimized_tokens": report.optimized_tokens,
        "reduction_percent": report.reduction_percent
    }
