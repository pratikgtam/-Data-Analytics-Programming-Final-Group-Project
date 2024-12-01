from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

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
    plt.close()  # Close the figure

    # Render chart template
    return render_template("chart.html", image_url="/static/traffic_volume.png")

@app.route("/line_chart")
def line_chart():
    # Generate a line chart
    query = """
    SELECT "Year", SUM("DailyTrafficVolume") AS total_traffic_volume
    FROM traffic_data
    GROUP BY "Year"
    ORDER BY "Year" ASC;
    """
    df = pd.read_sql(query, engine)

    # Create a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(df['Year'], df['total_traffic_volume'], marker='o', linestyle='-', color='skyblue')
    plt.title("Traffic Volume by Year")
    plt.xlabel("Year")
    plt.ylabel("Total Traffic Volume")
    plt.savefig("static/traffic_volume_line.png")  # Save chart as an image
    plt.close()  # Close the figure

    # Render chart template
    return render_template("chart.html", image_url="/static/traffic_volume_line.png")

@app.route("/avg_daily_volume_by_month")
def avg_daily_volume_by_month():
    # Generate a bar chart for average daily traffic volume by month
    query = """
    SELECT EXTRACT(MONTH FROM "Date") AS month, AVG("DailyTrafficVolume") AS avg_daily_volume
    FROM traffic_data
    GROUP BY month
    ORDER BY month ASC;
    """
    df = pd.read_sql(query, engine)

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df['month'], df['avg_daily_volume'], color='skyblue')
    plt.title("Average Daily Traffic Volume by Month")
    plt.xlabel("Month")
    plt.ylabel("Average Daily Traffic Volume")
    plt.xticks(range(1, 13))
    plt.savefig("static/avg_daily_volume_by_month.png")  # Save chart as an image
    plt.close()  # Close the figure

    # Render chart template
    return render_template("chart.html", image_url="/static/avg_daily_volume_by_month.png")

@app.route("/volume_by_day_of_week")
def volume_by_day_of_week():
    # Generate a bar chart for traffic volume by day of the week
    query = """
    SELECT EXTRACT(DOW FROM "Date") AS day_of_week, SUM("DailyTrafficVolume") AS total_volume
    FROM traffic_data
    GROUP BY day_of_week
    ORDER BY day_of_week ASC;
    """
    df = pd.read_sql(query, engine)

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df['day_of_week'], df['total_volume'], color='skyblue')
    plt.title("Traffic Volume by Day of the Week")
    plt.xlabel("Day of the Week")
    plt.ylabel("Total Traffic Volume")
    plt.xticks(range(7), ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    plt.savefig("static/volume_by_day_of_week.png")  # Save chart as an image
    plt.close()  # Close the figure

    # Render chart template
    return render_template("chart.html", image_url="/static/volume_by_day_of_week.png")

@app.route("/volume_by_hour_of_day")
def volume_by_hour_of_day():
    # Generate a bar chart for traffic volume by hour of the day
    query = """
    SELECT EXTRACT(HOUR FROM "Time") AS hour_of_day, SUM("DailyTrafficVolume") AS total_volume
    FROM traffic_data
    GROUP BY hour_of_day
    ORDER BY hour_of_day ASC;
    """
    df = pd.read_sql(query, engine)

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df['hour_of_day'], df['total_volume'], color='skyblue')
    plt.title("Traffic Volume by Hour of the Day")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Total Traffic Volume")
    plt.xticks(range(24))
    plt.savefig("static/volume_by_hour_of_day.png")  # Save chart as an image
    plt.close()  # Close the figure

    # Render chart template
    return render_template("chart.html", image_url="/static/volume_by_hour_of_day.png")

if __name__ == "__main__":
    app.run(debug=True)