# Functions for creating map and table
def find_top_confirmed(n = 15):
    import pandas as pd
    # Extract your dataframe
    covid_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/07-19-2022.csv')
    country_covid = covid_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    confirmed_df = country_covid.nlargest(15, 'Confirmed')[['Confirmed']]
    return confirmed_df

cdf = find_top_confirmed().to_html()

import pandas as pd
covid_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/07-19-2022.csv')
covid_df.head()

#!pip install folium
import folium
map = folium.Map(location = [33.93911, 67.709953],
          zoom_start = 10)

# Add your circle object
folium.Circle(location = [33.93911, 67.709953], radius = 1000, color = 'red', fill = True,
             popup = 'confirmed {}'.format(20)).add_to(map)

# Adding circles to each given lat/long
def circle_maker(x):
    folium.Circle(location = [x[0], x[1]], 
                  radius = 10000,
                  color = 'red',
                  fill = True,
                  popup = '{}\nConfirmed Cases: {}'.format(x[3], x[2])).add_to(map)

# Drops all NA's in lat/long
covid_df_long = covid_df.dropna(subset=['Long_'])
covid_df_clean = covid_df.dropna(subset=['Lat'])

covid_df_clean = covid_df_clean.merge(covid_df_long, how = "right")
# Subset dataframe based on the 4 columns then apply it
covid_df_clean[['Lat', 'Long_', 'Confirmed', 'Combined_Key']].apply(lambda x: circle_maker(x), axis = 1)

html_map = map._repr_html_()


# Flask w/ MongoDB
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/covid_db"
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html', table = cdf, cmap = html_map)

if __name__ == '__main__':
    app.run(debug=True)
