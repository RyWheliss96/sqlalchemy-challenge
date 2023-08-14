# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    one_year_earlier = '2016-08-23'

    # Perform a query to retrieve the data and precipitation scores
    precip_scores = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d",Measurement.date)>= one_year_earlier).\
        order_by((Measurement.date).desc()).all()

    # Convert the query results from your precipitation analysis 
    # (i.e. retrieve only the last 12 months of data) 
    # to a dictionary using date as the key and prcp as the value.
    results = []
    for date, prcp in precip_scores:
        results.append({date:prcp})

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list    
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most-active station for the previous year of data.
    Return a JSON list of temperature observations for the previous year."""

    # Calculate the date one year from the last date in data set.
    one_year_earlier = '2016-08-23'

    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station
    results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(func.strftime("%Y-%m-%d",Measurement.date)>= one_year_earlier).\
        all()


    session.close()

    # Convert list of tuples into normal list    
    temps = []
    for date,temp in results:
        temps.append({date:temp})

    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, 
    the average temperature, 
    and the maximum temperature for a specified start or start-end range.."""


    # Using the start value calculate the lowest, highest, and average temperature.
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d",Measurement.date) >= start).\
        all()


    session.close()

    # Convert list of tuples into normal list    
    temps = list(np.ravel(results))

    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, 
    the average temperature, 
    and the maximum temperature for a specified start or start-end range.."""


    # Using the start value calculate the lowest, highest, and average temperature.
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d",Measurement.date) >= start).\
        filter(func.strftime("%Y-%m-%d",Measurement.date) <= end).\
        all()


    session.close()

    # Convert list of tuples into normal list    
    temps = list(np.ravel(results))

    return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)
