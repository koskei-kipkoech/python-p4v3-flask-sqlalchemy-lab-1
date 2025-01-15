# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,session
from flask_migrate import Migrate
from sqlalchemy.orm import Session
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquakes(id):
    with Session(db.engine) as session:
        earthquake = session.get(Earthquake,id)
        if earthquake:
            return jsonify({
                "id": earthquake.id,
                "location":earthquake.location,
                "magnitude":earthquake.magnitude,
                "year":earthquake.year
            })
        else:
            return jsonify({"message": f'Earthquake {id} not found.'}),404
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude>= magnitude).all()
    quake_data = [{
        "id": quakes.id,
        "location": quakes.location,
        "magnitude": quakes.magnitude,
        "year": quakes.year
    }for quakes in quakes]

    return jsonify({
        "count": len(quakes),
        "quakes": quake_data
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
