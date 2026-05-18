# simple-mcp

A minimal MCP server built with [FastMCP](https://github.com/jlowin/fastmcp) and served over **streamable-http**.

## Tools

| Tool | Input | Description |
|---|---|---|
| `ping` | — | Returns `pong`. Health check. |
| `echo` | `message: str` | Reflects the message back in multiple cases. |
| `calculator` | `operation, a, b` | `add` / `subtract` / `multiply` / `divide` on two numbers. |
| `current_time` | — | Returns local date and time (`YYYY-MM-DD HH:MM:SS`). |
| `current_weather` | `location: str` | Current temperature and wind speed for any city via Open-Meteo. |

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

See [SETUP.md](SETUP.md) for full installation and configuration instructions.

## Quick start

```bash
uv run server.py
```

Server listens on `http://127.0.0.1:8000/mcp` by default.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `HOST` | `127.0.0.1` | Bind address |
| `PORT` | `8000` | Bind port |

Copy `.env.example` to `.env` and edit as needed.


**TOOLS AND TECHNOLOGIES USED**
Python 3.12
 The main programming language used to build the MCP server and implement tool logic.
uv
 A fast Python package manager used to create virtual environments, install dependencies, and run the project in a reproducible way.
FastMCP
 A framework for building MCP servers. It allows defining tools using decorators and exposes them over HTTP using streamable transport so AI clients can access them.
SQLite
 A lightweight local database used to store expense records. It enables persistent storage of user transactions.
aiosqlite
 An asynchronous SQLite driver used to perform database operations without blocking the server.
httpx
 An asynchronous HTTP client used for external API calls (if needed in future extensions like weather or currency conversion).
ngrok
 A tunneling tool that exposes the local MCP server to the internet using a public HTTPS URL. This allows ChatGPT Developer Mode to access the server.
ChatGPT Developer Mode (MCP Connector)
 Used to connect the MCP server to ChatGPT. It enables ChatGPT to automatically discover and use tools exposed by the server.

SETUP AND INSTALLATION INSTRUCTIONS
Step 1: Create project folder
 Create a new folder and initialize the project using uv.
Step 2: Set Python version
 Ensure Python 3.12 is selected by creating a .python-version file.
Step 3: Install dependencies
 Install required packages using uv add:
·	fastmcp
·	httpx
·	python-dotenv
·	aiosqlite
Step 4: Create environment file
 Create a .env file with the following configuration:
 HOST=0.0.0.0
 PORT=8000
Step 5: Create server file
 Create a server.py file that defines MCP tools:
·	log_expense
·	summarise_spending
·	budget_alert
These tools interact with a local SQLite database.
Step 6: Initialize database
 On startup, the server creates an expenses table in SQLite if it does not already exist.



**SETUP AND INSTALLATION**
Step 1: Create project folder
Create a new folder and initialize the project using uv.

Step 2: Set Python version
Ensure Python 3.12 is selected by creating a .python-version file.

Step 3: Install dependencies
Install required packages using uv add:

fastmcp
httpx
python-dotenv
aiosqlite

Step 4: Create environment file
Create a .env file with the following configuration:
HOST=0.0.0.0
PORT=8000

Step 5: Create server file
Create a server.py file that defines MCP tools:

log_expense
summarise_spending
budget_alert

These tools interact with a local SQLite database.

Step 6: Initialize database
On startup, the server creates an expenses table in SQLite if it does not already exist.

