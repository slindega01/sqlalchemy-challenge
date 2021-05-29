from flask import Flask, jsonify
import datetime as dt
import numpy as np 
import pandas as pd
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///Hawaii.sqlite",connect_args={'check_same_thread':False})
Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurements = Base.classes.measurement
session = Session(engine)



app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available API routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    maxDate = dt.date(2017,8,23)
    year_ago = maxDate-dt.timedelta(days=365)

    past_temp = (session.query(Measurements.date,Measurements.prcp )
                .filter(Measurements.date<=maxDate)
                .filter(Measurements.date>=year_ago)
                .order_by(Measurements.date).all())
    precip = {date:prcp for date, prcp in past_temp}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    maxDate1 = dt.date(2017,8,23)
    year_ago1 = maxDate1-dt.timedelta(days=365)
    last_year = (session.query(Measurements.date, Measurements.tobs)
                .filter(Measurements.station == 'USC00519281')
                .filter(Measurements.date<= maxDate1)
                .filter(Measurements.date>=year_ago1)
                .order_by(Measurements.tobs).all())
    return jsonify(last_year)


@app.route("/api/v1.0/<start>")
def trip(start):
    date_entry = input("Enter date in YYYY-MM-DD format")
    year,month,day = map(int,date_entry.split('-'))
    start_date = dt.date(year, month, day)
    
    
    tobs_only = session.query(func.min(Measurements.tobs),func.avg(Measurements.tobs),func.max(Measurements.tobs)).\
                filter(Measurements.date >=start_date).all()
    
   

    return jsonify(tobs_only)


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    start_date1 = dt.date(2010,1,1)
    end_date = dt.date(2017,8,23)
    tobs_start_end = session.query(func.min(Measurements.tobs),func.avg(Measurements.tobs),func.max(Measurements.tobs)).\
                filter(Measurements.date >=start_date1).filter(Measurements.date<=end_date).all()
    

    return jsonify(tobs_start_end)


if __name__ == "__main__":
    app.run(debug=True)
    

