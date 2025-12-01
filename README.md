# Mini Stats API
- Will Gurley
  
## 1) Executive Summary

### Problem
Many people want to quickly get statistics and information about a CSV file without any previous knowledge of programming or data analysis. Existing tools can sometimes be too complex or require installation of software.

### Solution
Mini Stats API is a simple web-based application that allows users to upload a CSV file and receive basic statistics and insights about the data contained within the file. The application will provide summary statistics such as mean, median, mode, standard deviation, and data type information for each column in the CSV file. Also, it will generate simple visualizations like histograms and box plots for numerical data.

## 2) System Overview

### Course Concepts:
- Flask API: The application will be built using Flask to create a RESTful API that handles file uploads and returns statistical summaries.
- Data Analysis with Pandas: The Pandas library will be used to read the CSV files and perform data analysis
- Data Visualization with Matplotlib/Seaborn: These libraries will be used to create visualizations of the data.
- HTML/CSS/JavaScript: The front-end will be built using basic web technologies to create a user-friendly interface for file uploads and displaying results.

### Architecture Diagram:
```
[User] --> [Flask API] --> [Pandas Data Analysis] --> [Matplotlib/Seaborn Visualizations]
```

### Data/Models/Services: 
- Data: CSV files uploaded by users.
- Models: None (statistical calculations will be performed directly on the data).
- Services: Flask API to handle requests and responses.

## 3) How to Run (Local)

### Docker

```bash
# build
docker build -t mini-stats-api:latest .

# run
docker run --rm -p 8080:8080 mini-stats-api:latest

# health check
curl http://localhost:8080/health
```

After starting the server, open `http://localhost:8080/` in your browser to access the web interface.

**Note**: If you have a `.env` file with environment variables, you can use:
```bash
docker run --rm -p 8080:8080 --env-file .env mini-stats-api:latest
```

### Alternative: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python src/app.py

# Health check
curl http://localhost:8080/health
```

