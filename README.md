# Mini Stats API

A Flask-based REST API for uploading CSV files and performing statistical analysis.

## Features

- Upload CSV files via POST endpoint
- Get column information and statistical summaries
- Filter data by column values
- Generate histograms for numeric columns
- Query individual column values

## Setup

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

```bash
python src/app.py
```

The server will start on `http://localhost:8080`

### Running with Docker

```bash
docker build -t mini-stats-api:latest .
docker run --rm -p 8080:8080 --env-file .env mini-stats-api:latest
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /upload` - Upload a CSV file (requires `file` in form-data)
- `GET /columns` - Get list of all columns
- `GET /summary` - Get statistical summary of numeric columns
- `GET /column/<col>` - Get all values for a specific column
- `GET /filter?col=<name>&value=<value>` - Filter rows by column value
- `GET /plot/<col>` - Generate histogram PNG for a numeric column
- `GET /meta` - Get metadata about the uploaded dataset

## Testing

Run the test suite:

```bash
pytest tests/
```

## Project Structure

```
final_project/
├── src/
│   └── app.py          # Main Flask application
├── tests/
│   └── test_smoke.py    # Smoke tests
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

