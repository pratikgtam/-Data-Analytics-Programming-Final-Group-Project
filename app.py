from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Database connection
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'database-city-of-barrie-traffic.c3cygy42s6pf.us-east-1.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = 'Pass123$'
DATABASE = 'postgres'
PORT = 5432

connection_url = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(connection_url)

@app.route("/")
def home():
    # Query total records
    query = "SELECT COUNT(*) AS total_records FROM traffic_data;"
    result = pd.read_sql(query, engine)
    total_records = result.iloc[0]['total_records']

    # Render the homepage
    return render_template("index.html", total_records=total_records)

@app.route("/results")
def results():
    # Query traffic volume by year
    query = """
    SELECT "Year", SUM("DailyTrafficVolume") AS total_traffic_volume
    FROM traffic_data
    GROUP BY "Year"
    ORDER BY "Year" ASC;
    """
    df = pd.read_sql(query, engine)

    # Convert data to a list of dictionaries for rendering
    data = df.to_dict(orient="records")
    return render_template("results.html", data=data)

# Add the chart route here
@app.route("/chart")
def chart():
    # Generate a bar chart
    query = """
    SELECT "Year", SUM("DailyTrafficVolume") AS total_traffic_volume
    FROM traffic_data
    GROUP BY "Year"
    ORDER BY "Year" ASC;
    """
    df = pd.read_sql(query, engine)

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df['Year'], df['total_traffic_volume'], color='skyblue')
    plt.title("Traffic Volume by Year")
    plt.xlabel("Year")
    plt.ylabel("Total Traffic Volume")
    plt.savefig("static/traffic_volume.png")  # Save chart as an image

    # Render chart template
    return render_template("chart.html", image_url="/static/traffic_volume.png")

if __name__ == "__main__":
    app.run(debug=True)