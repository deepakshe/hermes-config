---
name: pentagi-deployment
description: Deploy PentAGI pentesting on Windows with Docker and Ollama.
tags: [pentagi, docker, ollama, windows, wsl2, penetration-testing]
---

# PentAGI Deployment Skill

Deploy PentAGI — an autonomous AI penetration testing platform — on Windows 11 with local Ollama models.

## Trigger Conditions

- User asks to install, set up, or run PentAGI
- User wants AI penetration testing with local LLM models
- Docker Desktop installation or WSL2 configuration is needed on Windows

## Prerequisites

- Windows 10/11 (64-bit)
- Administrator privileges
- At least 4GB RAM (8GB+ recommended)
- Internet access for image downloads

## Deployment Overview

PentAGI runs via Docker Compose with these core services:
- `pentagi` — Main app (Go backend + React UI), port 8443
- `pgvector` — PostgreSQL with pgvector, port 5432
- `scraper` — Isolated browser for web intel, port 9443
- `pgexporter` — Prometheus metrics, port 9187

## Step 1: Install Docker Desktop on Windows

### Enable Windows Features

```powershell
# Run as Administrator in PowerShell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
```

Then **restart the computer**.

### Set WSL2 as Default

```cmd
wsl --set-default-version 2
```

### Verify Docker Installation

After restart, Docker Desktop is often already installed. Check:

```cmd
docker --version
docker compose version
docker info
```

### Common Pitfall: `choco install docker-desktop` Fails with MSI Error 1603

If Chocolatey gives error 1603, don't panic. The MSI may have partially installed Docker. After the WSL2 restart, check if `docker.exe` is available at:
```
C:\Users\<user>\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe
```

If `docker info` works, proceed — no further installation needed.

### Common Pitfall: `winget` False Positive

`winget install Docker.DockerDesktop` may say "already installed" when it's not. Verify with `docker --version` before trusting winget's output.

## Step 2: Configure PentAGI Environment

### Create Working Directory

```cmd
mkdir pentagi
cd pentagi
```

### Download Configuration Files

```cmd
curl -L -o .env https://raw.githubusercontent.com/vxcontrol/pentagi/master/.env.example
curl -L -o docker-compose.yml https://raw.githubusercontent.com/vxcontrol/pentagi/master/docker-compose.yml
```

### Configure Ollama Provider

Edit `.env` to use your local Ollama:

```env
OLLAMA_SERVER_URL=http://host.docker.internal:11434
OLLAMA_SERVER_API_KEY=
OLLAMA_SERVER_MODEL=mistral
OLLAMA_SERVER_PULL_MODELS_ENABLED=false
OLLAMA_SERVER_LOAD_MODELS_ENABLED=true

EMBEDDING_URL=http://host.docker.internal:11434
EMBEDDING_MODEL=mistral
EMBEDDING_PROVIDER=ollama
```

**Important:** `host.docker.internal` resolves to the host machine from inside Docker containers on Windows.

### Common Pitfall: Config File Mount Creates Directories

On Windows/WSL2, Docker volume mounts of individual files (like `./example.ollama.provider.yml`) can create **directories** instead of files, causing PentAGI to fail with `read /opt/pentagi/conf/ollama.provider.yml: is a directory`.

**Workaround:** Don't use `OLLAMA_SERVER_CONFIG_PATH`. PentAGI works fine with just `OLLAMA_SERVER_URL` + `OLLAMA_SERVER_MODEL` set.

If you must use a config file, create the file first, then mount it. But the URL+model approach is simpler and more reliable.

## Step 3: Launch PentAGI

```cmd
docker-compose up -d
```

### Verify Containers

```cmd
docker ps
```

Expected output: `pentagi`, `pgvector` (healthy), `scraper`, `pgexporter` all running.

### Check Logs

```cmd
docker logs pentagi --tail 30
```

Look for: `API server listening on 0.0.0.0:8443` and `Starting server with TLS enabled`.

If you see `LLM provider controller initialization failed`, double-check your Ollama URL and that Ollama is running on the host.

## Step 4: Access PentAGI

1. Open browser → **https://localhost:8443**
2. Accept the self-signed TLS certificate warning (click Advanced → Proceed)
3. Create admin account on first login
4. Go to Settings → Providers to verify Ollama connection

## Troubleshooting

### PentAGI Keeps Restarting

```cmd
docker logs pentagi --tail 50
```

Common causes:
- **Embedder error**: Set `EMBEDDING_URL`, `EMBEDDING_MODEL`, `EMBEDDING_PROVIDER` in `.env`
- **Config file is directory**: Remove `OLLAMA_SERVER_CONFIG_PATH` from `.env`
- **Database not ready**: Wait for `pgvector` to show "healthy" in `docker ps`

### Ollama Not Reachable from Container

Ensure Ollama is listening on all interfaces or at least on the Docker bridge. Test from host:
```cmd
curl http://localhost:11434/api/tags
```

If using a custom Ollama port or remote server, update `OLLAMA_SERVER_URL` accordingly.

### Port Conflicts

If port 8443 is in use, edit `docker-compose.yml`:
```yaml
ports:
  - "127.0.0.1:<new-port>:8443"
```

## Architecture Notes

- PentAGI agents run in sandboxed Docker containers
- All command output is stored in PostgreSQL with pgvector
- The scraper provides isolated browser access for web intelligence
- Knowledge Graph (Graphiti/Neo4j) is optional and disabled by default
- Langfuse integration is optional for LLM observability

## References

- [Official PentAGI README](https://github.com/vxcontrol/pentagi)
- [PentAGI Installation Guide](https://github.com/vxcontrol/pentagi/blob/master/examples/guides/installation_configuration.md)
- [Ollama Provider Config](https://github.com/vxcontrol/pentagi/blob/master/examples/configs/ollama-llama318b.provider.yml)
