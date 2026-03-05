# ChartDB - Docker Setup

[ChartDB](https://github.com/chartdb/chartdb) is an open-source database diagram editor. Visualize and design your database schema with a single query—no installations or database password required.

## Quick Start

### Using Pre-built Image

```bash
docker run -p 8080:80 ghcr.io/chartdb/chartdb:latest
```

Open **http://localhost:8080** in your browser.

### Build from Source

```bash
git clone https://github.com/chartdb/chartdb.git
cd chartdb
docker build -t chartdb .
docker run -p 8080:80 chartdb
```

## How to Use

1. Go to [ChartDB.io](https://chartdb.io) or your local instance
2. Choose your database (PostgreSQL, MySQL, SQL Server, etc.)
3. Run the provided "magic query" in your database
4. Copy the resulting JSON into ChartDB
5. View and edit your schema diagram

## Run in Background

```bash
# Run detached (background)
docker run -d -p 8080:80 --name chartdb ghcr.io/chartdb/chartdb:latest

# Stop the container
docker stop chartdb

# Remove the container
docker rm chartdb
```

## Docker Compose

```bash
# Copy environment template and configure (optional)
cp .env.example .env
# Edit .env to add your OPENAI_API_KEY if you have one

# Start the stack (runs in background)
docker compose up -d

# Stop and remove containers
docker compose down
```

See `docker-compose.yml` for the configuration.

## Configuration

Configuration is done via environment variables. Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

| Environment Variable | Description |
|---------------------|-------------|
| `OPENAI_API_KEY`   | Optional—enables AI-powered schema export. Leave empty to run without AI. |
| `DISABLE_ANALYTICS` | Set to `true` to disable analytics (default: `true`) |

## OpenAI API Key (Optional)

ChartDB works fully without an API key. If you have an **OpenAI API key**, you can optionally enable AI-powered schema export (e.g., converting DDL between MySQL and PostgreSQL).

**Without key:** Schema import, diagram editing, and manual export work normally.

**With key:** AI-assisted export to different SQL dialects.

### Using with Docker Run

```bash
# Run with AI features (if you have a key)
docker run -e OPENAI_API_KEY=sk-your-key-here -p 8080:80 ghcr.io/chartdb/chartdb:latest

# Run in background with AI
docker run -d -e OPENAI_API_KEY=sk-your-key-here -p 8080:80 --name chartdb ghcr.io/chartdb/chartdb:latest
```

### Using with Docker Compose

1. Copy the example: `cp .env.example .env`
2. Add your key to `.env`: `OPENAI_API_KEY=sk-your-key-here`
3. Run: `docker compose up -d`

If `OPENAI_API_KEY` is empty or omitted, ChartDB runs without AI features—no errors.

## Examples

**Run on a custom port:**
```bash
docker run -p 3000:80 ghcr.io/chartdb/chartdb:latest
```

**Run with analytics disabled:**
```bash
docker run -e DISABLE_ANALYTICS=true -p 8080:80 ghcr.io/chartdb/chartdb:latest
```

## Supported Databases

- PostgreSQL (including Supabase, Timescale)
- MySQL
- SQL Server
- MariaDB
- SQLite (including Cloudflare D1)
- CockroachDB
- ClickHouse

## License

ChartDB is licensed under the [AGPL-3.0](https://github.com/chartdb/chartdb/blob/main/LICENSE) license.
