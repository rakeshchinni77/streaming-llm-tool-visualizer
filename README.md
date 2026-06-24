# streaming-llm-tool-visualizer

A scaffolded repository for a full-stack streaming LLM tool visualizer. This project is designed to visualize LLM reasoning, tool usage, and real-time streaming output via a React frontend and FastAPI backend.

## Tech Stack

- Frontend: React, Vite
- Backend: FastAPI, Python 3.10.11
- Streaming: Server-Sent Events (SSE)
- Containerization: Docker, Docker Compose

## Requirements

- Python 3.10.11
- Node.js LTS
- Docker Desktop

## Architecture Overview

The system is structured as a monorepo with a React client and a Python backend. The backend proxies requests to an LLM provider, manages tool invocation logic, and streams partial results back to the frontend using SSE. The frontend renders streaming assistant text, displays tool execution blocks, and shows context token monitoring.

## Setup

Coming Soon

## Folder Structure

- `.env` - runtime environment configuration
- `.env.example` - example environment variables
- `docker-compose.yml` - service orchestration
- `submission.json` - evaluation API key payload
- `backend/` - FastAPI application and backend service
- `frontend/` - React application and UI code
- `docs/` - project documentation and architecture artifacts
