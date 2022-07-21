# Import your dependancies
from flask import Flask, render_template, redirect
import flask_functions
from sqlalchemy import create_engine
import pandas as pd

covid_api_url = "https://covidtracking.com/data/api"
covid_table_name = "sharks1"
covid_csv_path = "USA COVID DATA.csv"

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def index():
  return render_template("SharkTracker.html")

@app.route("/sources")  
def sources():
  return render_template("sources.html")

@app.route("/charts")
def charts():
  return render_template("charts.html")
  
@app.route("/update")
def update_data():
    covid_df = flask_functions.covid_data(covid_api_url, "2020-01-01", "2021-07-01")
    flask_functions.load_database(covid_df, covid_table_name, "data/sharks/australia.sqlite")

    covid_df.to_csv("USA COVID DATA.csv")

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)