# Mini Stats API

A Flask-based web application for uploading CSV files and performing statistical analysis. The application provides both a user-friendly web interface and a REST API for programmatic access.

## Features

### Web Interface
- **Upload CSV files** via drag-and-drop or file browser
- **View dataset information** including filename, row count, column names, and upload timestamp
- **Browse columns** with a complete list of all available columns
- **Statistical summary** with descriptive statistics (count, mean, std, min, 25%, 50%, 75%, max) for numeric columns
- **View column data** to inspect individual column values and data types
- **Filter data** by column values to find specific rows
- **Generate histograms** for numeric columns with interactive visualization

### REST API Endpoints
- `GET /` - Web interface homepage
- `GET /health` - Health check endpoint
- `POST /upload` - Upload a CSV file (requires `file` in form-data)
- `GET /meta` - Get metadata about the uploaded dataset
- `GET /columns` - Get list of all columns
- `GET /summary` - Get statistical summary of numeric columns
- `GET /column/<col>` - Get all values for a specific column
- `GET /filter?col=<name>&value=<value>` - Filter rows by column value (returns up to 100 rows)
- `GET /plot/<col>` - Generate histogram PNG for a numeric column

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

Open your browser and navigate to `http://localhost:8080/` to access the web interface.

### Running with Docker

```bash
docker build -t mini-stats-api:latest .
docker run --rm -p 8080:8080 --env-file .env mini-stats-api:latest
```

## Usage

### Web Interface

1. Start the server (see above)
2. Open `http://localhost:8080/` in your browser
3. Upload a CSV file by dragging and dropping or clicking to browse
4. Once uploaded, you can:
   - View dataset information and column list
   - Click "Load Summary" to see statistical summaries
   - Select a column and click "View Column" to see all values
   - Filter data by selecting a column and entering a value
   - Generate histograms for numeric columns

### API Usage

#### Upload a CSV file
```bash
curl -X POST http://localhost:8080/upload \
  -F "file=@your_data.csv"
```

#### Get column list
```bash
curl http://localhost:8080/columns
```

#### Get statistical summary
```bash
curl http://localhost:8080/summary
```

#### Get column values
```bash
curl http://localhost:8080/column/ColumnName
```

#### Filter data
```bash
curl "http://localhost:8080/filter?col=ColumnName&value=some_value"
```

#### Generate histogram
```bash
curl http://localhost:8080/plot/ColumnName -o histogram.png
```

## Configuration

The application supports the following environment variables:

- `PORT` - Server port (default: 8080)
- `FLASK_DEBUG` - Enable debug mode (default: "0")
- `UPLOAD_KEY` - Optional API key for upload endpoint (set `X-Upload-Key` header)
- `MAX_ROWS` - Maximum number of rows allowed in uploaded CSV (default: 200000)

## Testing

Run the test suite:

```bash
pytest tests/
```

## Project Structure

```
final_project/
├── src/
│   ├── app.py              # Main Flask application
│   └── templates/
│       └── index.html      # Web interface template
├── tests/
│   └── test_smoke.py       # Smoke tests
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── run.sh                  # Docker run script
└── README.md               # This file
```

## Technology Stack

- **Flask** - Web framework
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Data visualization
- **HTML/CSS/JavaScript** - Frontend interface

## Notes

- The application stores data in-memory (one dataset at a time)
- Filtered results are limited to 100 rows for performance
- Histograms are only available for numeric columns
- The web interface automatically updates column dropdowns after file upload
