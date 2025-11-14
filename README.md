# Mini Stats API - Case Study

## 1) Executive Summary

### Problem
Data analysts and researchers frequently need to quickly explore and analyze CSV datasets without installing heavy statistical software or writing custom scripts. The problem is providing an accessible, web-based tool that allows users to upload CSV files and immediately perform common statistical operations, data exploration, and visualization without technical barriers.

### Solution
Mini Stats API is a lightweight Flask-based web application that provides both a user-friendly web interface and REST API endpoints for CSV data analysis. Users can upload CSV files via drag-and-drop, view dataset metadata, explore columns, generate statistical summaries, filter data, and create histograms—all through an intuitive web interface. The application stores data in-memory for fast access and provides programmatic access via REST endpoints for integration with other tools.

## 2) System Overview

### Course Concept(s)
- **Web APIs (Flask)**: RESTful API design and HTTP endpoints
- **Data Processing (Pandas)**: CSV parsing, data manipulation, and statistical analysis
- **Data Visualization (Matplotlib)**: Dynamic histogram generation
- **Web Development**: HTML/CSS/JavaScript frontend with AJAX for asynchronous data loading

### Architecture Diagram
![Architecture Diagram](assets/architecture.png)

*Note: Architecture diagram should be placed in `/assets/architecture.png`*

The application follows a simple client-server architecture:
- **Frontend**: Single-page HTML application with JavaScript for dynamic content
- **Backend**: Flask REST API with in-memory data storage
- **Data Flow**: CSV upload → Pandas DataFrame → Statistical operations → JSON/PNG responses

### Data/Models/Services
- **Data Sources**: User-uploaded CSV files (any format supported by Pandas)
- **Data Storage**: In-memory Pandas DataFrame (single dataset at a time)
- **Data Size Limits**: Maximum 200,000 rows (configurable via `MAX_ROWS` environment variable)
- **Data Formats**: CSV files with any delimiter supported by Pandas
- **License**: Open source (see LICENSE file)
- **External Services**: None (fully self-contained)

## 3) How to Run (Local)

### Docker

```bash
# build
docker build -t mini-stats-api:latest .

# run
docker run --rm -p 8080:8080 --env-file .env mini-stats-api:latest

# health check
curl http://localhost:8080/health
```

After starting the server, open `http://localhost:8080/` in your browser to access the web interface.

### Alternative: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python src/app.py

# Health check
curl http://localhost:8080/health
```

## 4) Design Decisions

### Why this concept?
**Flask for Web API**: Flask was chosen for its simplicity, lightweight footprint, and ease of development. It provides just enough structure for REST endpoints without the overhead of larger frameworks like Django. The application's requirements (stateless operations, simple routing) align perfectly with Flask's strengths.

**Pandas for Data Processing**: Pandas is the industry standard for CSV manipulation and statistical analysis in Python. It provides robust CSV parsing, handles various data types automatically, and includes built-in statistical functions (describe(), filtering, etc.) that would otherwise require significant custom code.

**In-Memory Storage**: Using in-memory storage (single DataFrame) simplifies the architecture and provides fast access. This design decision aligns with the use case of analyzing one dataset at a time during exploratory analysis sessions.

**Alternatives Considered**:
- **Django**: Too heavyweight for a simple API; unnecessary ORM and admin features
- **FastAPI**: More modern but adds async complexity not needed for this use case
- **Database Storage**: Would add complexity; in-memory is sufficient for single-user analysis
- **Client-side Processing**: Would limit file size and require JavaScript data libraries

### Tradeoffs

**Performance**:
- ✅ Fast in-memory operations for datasets up to 200K rows
- ⚠️ Limited by available RAM for very large datasets
- ⚠️ Single-threaded Flask dev server (production would use Gunicorn)

**Cost**:
- ✅ Zero external service costs (no database, no cloud storage)
- ✅ Minimal resource requirements

**Complexity**:
- ✅ Simple architecture with minimal dependencies
- ✅ Easy to understand and maintain
- ⚠️ Single dataset limitation requires re-uploading to switch datasets

**Maintainability**:
- ✅ Clear separation of concerns (routes, helpers, data store)
- ✅ Standard Flask patterns
- ✅ Comprehensive error handling with JSON error responses

### Security/Privacy

**Secrets Management**:
- Optional `UPLOAD_KEY` environment variable for API key protection
- Environment variables used for configuration (`.env` file)

**Input Validation**:
- File type validation (CSV only)
- Row count limits to prevent memory exhaustion
- Column name validation in API endpoints
- Type-safe value casting for filtering operations

**PII Handling**:
- No persistent storage of uploaded data
- Data exists only in memory during server session
- No logging of sensitive data values
- Users responsible for data they upload

**Error Handling**:
- Comprehensive error handlers return JSON error responses
- Input validation prevents malformed requests
- Graceful handling of missing datasets

### Ops

**Logs/Metrics**:
- Python logging configured at INFO level
- Request logging via Werkzeug (Flask's development server)
- Upload events logged with file metadata (filename, row/column counts)

**Scaling Considerations**:
- Current design: Single-user, single-dataset
- For multi-user: Would need session management and per-user data stores
- For larger datasets: Would need database backend and pagination
- Production deployment: Use Gunicorn or uWSGI with multiple workers

**Known Limitations**:
- Single dataset in memory at a time
- No persistent storage (data lost on server restart)
- Filter results limited to 100 rows for performance
- Histograms only for numeric columns
- No authentication/authorization (if deployed publicly, use reverse proxy with auth)

## 5) Results & Evaluation

### Screenshots

*Note: Screenshots should be placed in `/assets/` directory*

- Web interface with uploaded dataset
- Statistical summary table
- Histogram visualization
- Filter results display

### Performance Notes

- **Upload Time**: < 1 second for datasets up to 10K rows
- **Summary Generation**: < 100ms for typical datasets
- **Histogram Generation**: < 200ms for numeric columns
- **Memory Footprint**: ~50-100MB base + ~1MB per 10K rows
- **Response Times**: All API endpoints respond in < 500ms for datasets under 50K rows

### Validation/Tests

**Smoke Tests** (`tests/test_smoke.py`):
- Health check endpoint
- File upload functionality
- Column listing
- Statistical summary generation
- Column data retrieval
- Data filtering
- Histogram generation

**Test Results**: All smoke tests pass, confirming core functionality works as expected.

**Manual Testing**:
- Tested with various CSV formats (comma-separated, different encodings)
- Validated with datasets ranging from 10 rows to 10K rows
- Confirmed error handling for invalid inputs
- Verified web interface interactivity across modern browsers

## 6) What's Next

### Planned Improvements

1. **Multi-Dataset Support**: Allow users to upload and switch between multiple datasets
2. **Persistent Storage**: Add optional database backend for saving datasets
3. **Advanced Visualizations**: Add scatter plots, box plots, and correlation matrices
4. **Data Export**: Allow users to download filtered/modified datasets
5. **Authentication**: Add user accounts and dataset ownership
6. **Pagination**: Implement pagination for large result sets
7. **Column Operations**: Add data transformation features (sorting, grouping, aggregations)

### Refactors

1. **Production Server**: Replace Flask dev server with Gunicorn for production deployment
2. **Error Handling**: More granular error messages and validation feedback
3. **Frontend Framework**: Consider React or Vue.js for more complex UI interactions
4. **API Versioning**: Add versioning to API endpoints for future compatibility
5. **Caching**: Implement response caching for frequently accessed data

### Stretch Features

1. **Real-time Collaboration**: Multiple users analyzing the same dataset simultaneously
2. **Machine Learning Integration**: Basic ML models (clustering, regression) on numeric data
3. **Data Profiling**: Automatic data quality reports and anomaly detection
4. **Export Formats**: Support for exporting to Excel, JSON, Parquet
5. **API Rate Limiting**: Protect against abuse with rate limiting
6. **WebSocket Support**: Real-time updates for long-running operations

---

## Additional Information

### API Endpoints

- `GET /` - Web interface homepage
- `GET /health` - Health check endpoint
- `POST /upload` - Upload a CSV file (requires `file` in form-data)
- `GET /meta` - Get metadata about the uploaded dataset
- `GET /columns` - Get list of all columns
- `GET /summary` - Get statistical summary of numeric columns
- `GET /column/<col>` - Get all values for a specific column
- `GET /filter?col=<name>&value=<value>` - Filter rows by column value (returns up to 100 rows)
- `GET /plot/<col>` - Generate histogram PNG for a numeric column

### Configuration

Environment variables:
- `PORT` - Server port (default: 8080)
- `FLASK_DEBUG` - Enable debug mode (default: "0")
- `UPLOAD_KEY` - Optional API key for upload endpoint
- `MAX_ROWS` - Maximum number of rows allowed (default: 200000)

### Project Structure

```
final_project/
├── src/
│   ├── app.py              # Main Flask application
│   └── templates/
│       └── index.html      # Web interface template
├── tests/
│   └── test_smoke.py       # Smoke tests
├── assets/                  # Screenshots and diagrams
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── run.sh                  # Docker run script
└── README.md               # This file
```
