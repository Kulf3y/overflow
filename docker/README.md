# Overflow Docker Deployment

Build the image from the repository root:

```bash
docker build -f docker/Dockerfile -t overflow:local .
```

Run the container:

```bash
docker run -p 8080:8080 overflow:local
```

Or use Docker Compose from the repository root:

```bash
docker compose -f docker/docker-compose.yml up --build
```

The gateway will be available at:

```text
http://127.0.0.1:8080/v1/health
```
