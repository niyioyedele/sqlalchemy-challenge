#copy all of imports
#%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates 
import numpy as np
import pandas as pd
import datetime as dt
#copy sql alchemy to set up engine and session
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
Msmt = Base.classes.measurement
Stn = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#set up flask
app = Flask(__name__)

#putinto functions
# def firstRow():
#     first_row =session.query(Stn).first()
#     first_row.__dict__
#     return   first_row.__dict__

#home screen
@app.route("/")
#display routes  for each function
def welcome():
    test = (f"Welcome to the Hawaii Climate Analyst<br/>"
    f"Available Routes: <br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end><br/>"
    
    
    )
    return test

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Msmt.date,Msmt.prcp).all()
    session.close

    precipitation = []

    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation.append(precipitation_dict)
        
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Stn.station,Stn.id,Stn.name).all()
    session.close
    stations = []

    for station,id,name in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict['id'] =id
        station_dict['name']
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)
    results = session.query(Msmt.date,Msmt.tobs,)\
        .filter(Msmt.date.between('2016-08-23', '2017-08-23'),Msmt.station=='USC00519281').all()
    session.close

    all_dates = list(np.ravel(results))

    return jsonify(all_dates)

start =input()
end = []

@app.route("/api/v1.0/<start>")
def datetemp():
    session = Session(engine)
    results = session.query(func.max(Msmt.tobs),func.min(Msmt.tobs),func.avg)\
        .filter(Msmt.dates >= start).all
    session.close

    all_temp = list(np.ravel(results))

    return jsonify(all_temp)

start =input()
end = input()

@app.route("/api/v1.0/<start>/<end>")
def travelnow():
    session = Session(engine)
    results = session.query(func.max(Msmt.tobs),func.min(Msmt.tobs),func.avg)\
        .filter(Msmt.dates.between(start.end)).all
    session.close

    all_temp = list(np.ravel(results))

    return jsonify(all_temp)

if __name__ == "__main__":
    app.run(debug=True)





        
        


    