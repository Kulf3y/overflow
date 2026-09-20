# Overflow Deployment

Overflow can run in multiple ways:

1. Python CLI
2. Local HTTP gateway
3. Docker container

## Python CLI

```powershell
python -m overflow.cli --help
```

## Local gateway

```powershell
python -m overflow.cli gateway
```

## Docker

```bash
docker build -f docker/Dockerfile -t overflow:local .
docker run -p 8080:8080 overflow:local
```

For Docker, the gateway binds to `0.0.0.0` inside the container.

Make sure you only expose it to trusted networks.
