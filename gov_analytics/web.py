from flask import Flask, render_template, send_file, request, jsonify
from .db import SessionLocal
from sqlalchemy import text
import plotly.io as pio
import plotly.express as px
import pandas as pd
import io
import os
import logging
from pathlib import Path
from .config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Fix template and static folder paths
base_dir = Path(__file__).resolve().parent.parent
template_folder = str(base_dir / "dashboard" / "templates")
static_folder = str(base_dir / "dashboard" / "static")

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)


def query_df(sql: str):
    db = SessionLocal()
    try:
        df = pd.read_sql(sql, db.bind)
        return df
    finally:
        db.close()


@app.route("/")
def index():
    # Overview KPIs
    try:
        total_b = query_df("SELECT COALESCE(SUM(beneficiaries),0) as total_beneficiaries FROM pmay;").iloc[0,0]
        total_pdays = query_df("SELECT COALESCE(SUM(person_days_generated),0) as mnrega_pd FROM mnrega;").iloc[0,0]
    except Exception:
        total_b = 0
        total_pdays = 0
    return render_template("overview.html", total_beneficiaries=int(total_b), total_pdays=int(total_pdays))


@app.route("/scheme")
def scheme_page():
    scheme = request.args.get("scheme", "pmay")
    year = request.args.get("year", None)
    year_filter = f"WHERE year={int(year)}" if year else ""
    
    # Use scheme-specific columns
    column_map = {
        "pmay": "COALESCE(beneficiaries,0)+COALESCE(houses_completed,0)",
        "mnrega": "COALESCE(person_days_generated,0)+COALESCE(job_cards,0)",
        "startup_india": "COALESCE(startups_supported,0)",
        "saubhagya": "COALESCE(households_electrified,0)"
    }
    
    score_col = column_map.get(scheme, "1")
    sql = f"SELECT state_name, SUM({score_col}) as score FROM {scheme} {year_filter} GROUP BY state_name"
    try:
        df = query_df(sql)
    except Exception as e:
        return render_template("scheme.html", scheme=scheme, chart_html=f"<p>Error: {e}</p>")
    
    if df.empty:
        return render_template("scheme.html", scheme=scheme, chart_html="<p>No data available. Run ETL first.</p>")
    
    fig = px.bar(df, x="state_name", y="score", title=f"{scheme} by state")
    chart_html = pio.to_html(fig, full_html=False)
    return render_template("scheme.html", scheme=scheme, chart_html=chart_html)


@app.route("/state_comparison")
def state_comparison():
    scheme = request.args.get("scheme", "pmay")
    year = request.args.get("year", None)
    year_filter = f"AND year={int(year)}" if year else ""
    
    # Use scheme-specific columns
    column_map = {
        "pmay": "COALESCE(beneficiaries,0)+COALESCE(houses_completed,0)",
        "mnrega": "COALESCE(person_days_generated,0)+COALESCE(job_cards,0)",
        "startup_india": "COALESCE(startups_supported,0)",
        "saubhagya": "COALESCE(households_electrified,0)"
    }
    
    score_col = column_map.get(scheme, "1")
    sql = f"SELECT state_code, state_name, SUM({score_col}) as score FROM {scheme} WHERE 1=1 {year_filter} GROUP BY state_code, state_name"
    df = query_df(sql)
    # Attempt choropleth if geojson available
    geojson_path = app.static_folder + "/data/india_states.geojson"
    geojson = None
    try:
        import json
        with open(geojson_path, "r", encoding="utf-8") as fh:
            geojson = json.load(fh)
    except Exception:
        geojson = None

    if geojson is not None and not df.empty:
        fig = px.choropleth_mapbox(df, geojson=geojson, locations="state_code", color="score", featureidkey="properties.state_code",
                                   mapbox_style="carto-positron", center={"lat": 22.0, "lon": 79.0}, zoom=3)
        chart_html = pio.to_html(fig, full_html=False)
    else:
        chart_html = "<p>GeoJSON not found or no data available.</p>"
    return render_template("state_comparison.html", chart_html=chart_html)


@app.route("/trends")
def trends():
    scheme = request.args.get("scheme", "pmay")
    state = request.args.get("state", None)
    
    # Use scheme-specific columns
    column_map = {
        "pmay": "COALESCE(beneficiaries,0)+COALESCE(houses_completed,0)",
        "mnrega": "COALESCE(person_days_generated,0)+COALESCE(job_cards,0)",
        "startup_india": "COALESCE(startups_supported,0)",
        "saubhagya": "COALESCE(households_electrified,0)"
    }
    
    score_col = column_map.get(scheme, "1")
    sql = f"SELECT year, SUM({score_col}) as val FROM {scheme}"
    if state:
        sql += f" WHERE state_name='{state}'"
    sql += " GROUP BY year ORDER BY year"
    df = query_df(sql)
    if df.empty:
        chart_html = "<p>No data available</p>"
    else:
        fig = px.line(df, x="year", y="val", title=f"{scheme} trend")
        chart_html = pio.to_html(fig, full_html=False)
    return render_template("trends.html", chart_html=chart_html)


@app.route("/export/<scheme>")
def export_csv(scheme: str):
    sql = f"SELECT * FROM {scheme}"
    df = query_df(sql)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return send_file(io.BytesIO(buf.getvalue().encode("utf-8")), mimetype="text/csv", as_attachment=True, download_name=f"{scheme}_cleaned.csv")


@app.route("/api/kpi/<scheme>")
def api_kpi(scheme: str):
    # Example simple KPI: total sum of numeric columns
    sql = f"SELECT SUM(COALESCE(beneficiaries,0)) as beneficiaries, SUM(COALESCE(houses_completed,0)) as houses_completed FROM {scheme}"
    try:
        df = query_df(sql)
        data = df.to_dict(orient="records")[0]
    except Exception:
        data = {}
    return jsonify(data)


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route("/trigger_etl", methods=["POST"])
def trigger_etl():
    """Trigger ETL for a scheme - requires secret token"""
    secret = request.form.get("secret") or request.headers.get("X-ETL-Secret")
    if not settings.ETL_TRIGGER_SECRET or secret != settings.ETL_TRIGGER_SECRET:
        return jsonify({"error": "Unauthorized"}), 401
    
    scheme = request.form.get("scheme")
    resource_id = request.form.get("resource_id")
    
    if not scheme or not resource_id:
        return jsonify({"error": "Missing scheme or resource_id"}), 400
    
    try:
        from .prefect_flows import etl_for_scheme
        import threading
        
        def run_etl():
            try:
                logger.info(f"Starting ETL for {scheme} with resource {resource_id}")
                result = etl_for_scheme(scheme, resource_id)
                logger.info(f"ETL completed: {result}")
            except Exception as e:
                logger.error(f"ETL failed: {e}", exc_info=True)
        
        thread = threading.Thread(target=run_etl, daemon=True)
        thread.start()
        
        return jsonify({"status": "ETL triggered", "scheme": scheme})
    except Exception as e:
        logger.error(f"Failed to trigger ETL: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
