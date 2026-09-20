# 🛡️ Overflow

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)

**Open-source AI governance and optimization middleware for European organizations.**

Overflow sits between your applications and AI providers to help control privacy, security, cost, routing, and auditability — all while respecting EU data sovereignty principles.

## ✨ Features

- **🔒 Privacy-First**: Automatically redacts PII (emails, phones, IBANs, custom patterns) before sending to AI models.
- **🛡️ Security Guardrails**: Blocks secrets, prompt injections, and jailbreak attempts.
- **📊 Token Optimization**: Reduces API costs through smart context compression and deduplication.
- **🎯 Policy-Driven Governance**: Enforce rules via JSON policies.
- **🔍 Tamper-Evident Audit Logs**: Hash-chained audit trail for compliance.
- **🌍 Provider Agnostic**: Works with OpenAI, Mistral, Ollama, or any OpenAI-compatible API.
- **🚀 FastAPI Gateway**: Modern HTTP API with auto-generated docs.
- **📊 Local Dashboard**: Test and monitor your pipeline in the browser.
- **🐳 Docker Ready**: Deploy anywhere with Docker.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git

### Installation

git clone https://github.com/Kulf3y/overflow.git
cd overflow
pip install -e python
cp .env.example .env

Edit your `.env` file to add your AI provider API key (OpenAI, Mistral, etc.).

### Run the Gateway

python -m overflow.cli gateway

Then open:
- **Dashboard**: http://127.0.0.1:8080/dashboard
- **API Docs**: http://127.0.0.1:8080/docs

## ⚖️ Legal Disclaimer

Overflow is a technical tool and does not provide legal advice. Compliance with the EU AI Act, GDPR, and other regulations requires human legal review.

---
**Built with ❤️ for European AI sovereignty**