# JARVIS v13 - Quickstart Guide

Get JARVIS running in 5 minutes.

## Prerequisites

- Python 3.10+
- pip or poetry
- Docker (optional, for containerized deployment)

## Option 1: Local Installation

### Step 1: Clone and Install

```bash
cd /workspace
pip install -r requirements.txt
```

### Step 2: Set Required Secrets

```bash
export JARVIS_API_TOKEN="your-api-token-here"
export JARVIS_SECURITY_SECRET="your-security-secret-here"
```

### Step 3: Run JARVIS

```bash
python main.py --mode development
```

### Step 4: Verify Health

```bash
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready
```

## Option 2: Docker Compose

### Step 1: Create docker-compose.yml

```yaml
version: "3.8"
services:
  jarvis:
    build: .
    ports:
      - "8000:8000"
    environment:
      - JARVIS_API_TOKEN=dev-token-change-in-production
      - JARVIS_SECURITY_SECRET=dev-secret-change-in-production
      - JARVIS_MODE=development
    volumes:
      - ./data:/app/data
      - ./config.json:/app/config.json
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Step 2: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py", "--api-only"]
```

### Step 3: Start with Docker

```bash
docker-compose up -d
```

### Step 4: Check Status

```bash
docker-compose ps
curl http://localhost:8000/health
```

## Configuration

### Security Settings (config.json)

By default, JARVIS runs in **fail-closed** mode:

- `allow_shell`: false
- `allow_code_execution`: false  
- `allow_network`: false
- `require_approval_for_high_risk`: true

To enable features for development:

```json
{
  "security": {
    "allow_shell": true,
    "allow_code_execution": true,
    "mode": "development"
  }
}
```

⚠️ **Warning**: Never use permissive settings in production!

## Health Endpoints

| Endpoint | Description |
|----------|-------------|
| `/health/live` | Liveness probe (is process alive?) |
| `/health/ready` | Readiness probe (ready for traffic?) |
| `/health` | Combined health status |

## Next Steps

- See `README.md` for full documentation
- Check `INSTALL.md` for detailed setup instructions
- Review `SECURITY.md` for security best practices
- Explore the API at `http://localhost:8000/docs`

## Troubleshooting

### Missing Secrets Error

```
SecretMissingError: Required secrets missing: JARVIS_API_TOKEN
```

**Solution**: Set the required environment variables before starting.

### Port Already in Use

```
OSError: [Errno 98] Address already in use
```

**Solution**: Change the port in config.json or stop the existing process.

### Import Errors

```
ImportError: No module named 'core'
```

**Solution**: Ensure you're running from the workspace directory and all dependencies are installed.
