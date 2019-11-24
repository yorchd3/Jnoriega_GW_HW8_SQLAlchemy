import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Jorge's API
#################################################

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"    
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
    )


@app.route("/api/v1.0/precipitations")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """onvert the query results to a Dictionary using date as the key and prcp as the value."""
    # Query 
    precipit = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-22', '2017-08-23')).all()

    data = []
    for result in precipit:
        preci_dictionary = {}
        preci_dictionary['Date'] = result.date
        preci_dictionary['Precipitation'] = result.prcp
        data.append(preci_dictionary)

    session.close()

    return jsonify(data)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all passengers
    station_qry = session.query(Station.station).all()

    station_data = []
    for result in station_qry:
        station_dictionary = {}
        station_dictionary['Station'] = result
        station_data.append(station_dictionary)

    session.close()

    return jsonify(station_data)
  

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all passengers
    tobs_qry = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between('2016-08-22', '2017-08-23')).all()

    tobs_data = []
    for result in tobs_qry:
        tobs_dictionary = {}
        tobs_dictionary['Date'] = result.date
        tobs_dictionary['Tobs'] = result.tobs
        tobs_data.append(tobs_dictionary)

    session.close()

    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def startdate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all passengers
    startdate_qry = session.query(func.min(Measurement.tobs).label('min'),\
                        func.max(Measurement.tobs).label('max'),\
                        func.avg(Measurement.tobs).label('ave')).filter(Measurement.date >= start).all()

    startdate_data = []
    for result in startdate_qry:
        start_dictionary = {}
        start_dictionary['Start_Date'] = start
        start_dictionary['Min'] = result.min
        start_dictionary['Max'] = result.max
        start_dictionary['Average'] = result.ave
        startdate_data.append(start_dictionary)

    session.close()

    return jsonify(startdate_data)

if __name__ == '__main__':
    app.run(debug=True)
