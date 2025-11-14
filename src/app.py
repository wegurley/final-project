# src/app.py
import io
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort, render_template
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Config
UPLOAD_KEY = os.getenv("UPLOAD_KEY", "")  # optional simple auth key
MAX_ROWS = int(os.getenv("MAX_ROWS", "200000"))  # guardrail

app = Flask(__name__)

# Global in-memory store for the uploaded DataFrame
DATASTORE = {
    "df": None,
    "uploaded_at": None,
    "filename": None
}

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mini-stats-api")

# Helpers
def ensure_df():
    if DATASTORE["df"] is None:
        abort(400, description="No dataset uploaded. Use POST /upload to upload a CSV.")

def safe_cast_value(value_str):
    # convert to int/float if possible, else leave as string
    try:
        if "." in value_str:
            return float(value_str)
        return int(value_str)
    except Exception:
        return value_str

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})

@app.route("/upload", methods=["POST"])
def upload():
    # Optional simple API key to prevent accidental public uploads
    key = request.headers.get("X-Upload-Key", "")
    if UPLOAD_KEY and key != UPLOAD_KEY:
        abort(401, description="Missing or invalid upload key.")

    if "file" not in request.files:
        abort(400, description="Missing 'file' in form-data.")
    f = request.files["file"]
    if f.filename == "":
        abort(400, description="Empty filename.")

    try:
        # read with pandas
        df = pd.read_csv(f)
    except Exception as e:
        logger.exception("Failed to read CSV")
        abort(400, description=f"Failed to read CSV: {str(e)}")


    # guard: limit rows
    if len(df) > MAX_ROWS:
        abort(400, description=f"CSV too large (rows > {MAX_ROWS}).")


    # store
    DATASTORE["df"] = df
    DATASTORE["uploaded_at"] = datetime.utcnow().isoformat() + "Z"
    DATASTORE["filename"] = f.filename

    logger.info(f"Uploaded file {f.filename} rows={len(df)} cols={len(df.columns)}")
    return jsonify({
        "status": "success",
        "rows": len(df),
        "columns": len(df.columns),
        "columns_list": df.columns.tolist()
    })

@app.route("/columns", methods=["GET"])
def columns():
    ensure_df()
    return jsonify({"columns": DATASTORE["df"].columns.tolist()})

@app.route("/summary", methods=["GET"])
def summary():
    ensure_df()
    df = DATASTORE["df"]
    # only numeric columns
    num = df.select_dtypes(include=["number"])
    if num.shape[1] == 0:
        return jsonify({"message": "No numeric columns present", "numeric_columns": []})
    desc = num.describe().to_dict()
    # convert numpy types to python native
    import json
    return jsonify(desc)

@app.route("/column/<col>", methods=["GET"])
def get_column(col):
    ensure_df()
    df = DATASTORE["df"]
    if col not in df.columns:
        abort(404, description=f"Column '{col}' not found.")
    # Return values as list (JSON serializable)
    series = df[col].where(pd.notnull(df[col]), None)  # preserve null as None
    return jsonify({
        "column": col,
        "dtype": str(series.dtype),
        "values": series.tolist()
    })

@app.route("/filter", methods=["GET"])
def filter_rows():
    ensure_df()
    df = DATASTORE["df"]
    col = request.args.get("col")
    val = request.args.get("value")
    if not col or val is None:
        abort(400, description="Require query params 'col' and 'value'")
    if col not in df.columns:
        abort(404, description=f"Column '{col}' not found.")
    # attempt numeric cast
    val_cast = safe_cast_value(val)
    filtered = df[df[col] == val_cast]
    # Return first 100 rows to avoid huge responses
    return jsonify({
        "filter": {"col": col, "value": val_cast},
        "rows_returned": min(len(filtered), 100),
        "rows_total": len(filtered),
        "data": filtered.head(100).to_dict(orient="records")
    })

@app.route("/plot/<col>", methods=["GET"])
def plot_col(col):
    ensure_df()
    df = DATASTORE["df"]
    if col not in df.columns:
        abort(404, description=f"Column '{col}' not found.")
    series = df[col].dropna()
    # only numeric allowed for histogram
    if not pd.api.types.is_numeric_dtype(series):
        abort(400, description=f"Column '{col}' is not numeric and cannot be plotted as histogram.")
    # make histogram
    fig, ax = plt.subplots(figsize=(6,4))
    ax.hist(series, bins=30)
    ax.set_title(f"Histogram: {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("count")
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype="image/png", as_attachment=False, download_name=f"{col}_hist.png")

# Simple endpoint to show current dataset meta
@app.route("/meta", methods=["GET"])
def meta():
    if DATASTORE["df"] is None:
        return jsonify({"loaded": False})
    return jsonify({
        "loaded": True,
        "filename": DATASTORE["filename"],
        "uploaded_at": DATASTORE["uploaded_at"],
        "rows": len(DATASTORE["df"]),
        "columns": DATASTORE["df"].columns.tolist()
    })

# Basic error handlers to return JSON errors
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def handle_errors(error):
    response = jsonify({
        "error": getattr(error, "name", "Error"),
        "message": getattr(error, "description", str(error))
    })
    response.status_code = getattr(error, "code", 500)
    return response

if __name__ == "__main__":
    # Local dev server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=os.getenv("FLASK_DEBUG", "0") == "1")

