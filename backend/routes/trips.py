from flask import Blueprint, request, jsonify
from backend.db import get_db

trips_bp = Blueprint('trips', __name__, url_prefix='/trips')

@trips_bp.route('/', methods=['POST'])
def create_trip():
    '''
    This function gets data about a trip from the user and checks if all the must have fields are filled in. 
    Then it checks if there is a user in the db which it can connect to.
    If the user exists and the data is complete a new trip is added to the aferent table. 
    '''
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'We need some info about your trip'}), 400
    
    must_have_fields =  ["user_id", "destination", "start_date", "end_date", "nr_people"]

    for f in must_have_fields:
        if f not in data:
            return jsonify({'error': f"Missing field: {f}"}), 400
        
    user_id = data["user_id"]
    destination = data["destination"]
    start_date = data["start_date"]
    end_date = data["end_date"]
    nr_people = data["nr_people"]

    if not destination:
        return jsonify({"error": "We need a destination"}), 400
    
    if int(nr_people) <= 0:
        return jsonify({"error": "We need at least one traveler"}), 400
    
    db = get_db()

    user = db.execute(
        'SELECT id FROM users WHERE id = ?', (user_id,)
    ).fetchone()

    if user is None:
        return jsonify({"error": "You must be a user"}), 400
    
    cursor = db.execute(
        """
        INSERT INTO Trips (user_id, destination, start_date, end_date, nr_people)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, destination, start_date, end_date, nr_people)
    )

    db.commit()

    return jsonify({
        'message': 'Your trip was created successfully :)',
        'trip_id': cursor.lastrowid
        }), 201
    
@trips_bp.route('/', methods=['GET'])
def get_trips():
    """
    Get all trips from DB and return a list of dictionaries with each trip's details.
    """
    db = get_db()

    trips = db.execute(
        "SELECT * FROM Trips"
    ).fetchall()

    trips_list = []
    for t in trips:
        trips_list.append({
            "trip_id": t['trip_id'],
            "user_id": t["user_id"],
            "destination": t["destination"],
            "start_date": t["start_date"],
            "end_date": t["end_date"],
            "nr_people": t["nr_people"],
            "is_random": t["is_random"]
            })
    
    return jsonify(trips_list), 200

@trips_bp.route('/<int:trip_id>', methods=['GET'])
def get_one_trip(trip_id: int):
    """
    Get one specific trip by its id. 
    If the trip does not exist, return an error message. 
    """
    db = get_db()

    trip = db.execute(
        "SELECT * FROM Trips WHERE trip_id = ?", (trip_id,)
    ).fetchone()

    if trip is None:
        return jsonify({"error": "Sorryyy! There is no trip :("}), 404
    
    return jsonify({
        "trip_id": trip['trip_id'],
            "user_id": trip["user_id"],
            "destination": trip["destination"],
            "start_date": trip["start_date"],
            "end_date": trip["end_date"],
            "nr_people": trip["nr_people"]
        }), 200

@trips_bp.route("/<int:trip_id>", methods = ['PUT'])
def update_trip(trip_id):
    """
    Update the details of one specific trip by its id. 
    If the trip does not exist, return an error message.
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "There's no change :("}), 400
    
    db = get_db()

    trip = db.execute(
        "SELECT * FROM Trips WHERE trip_ip = ?", (trip_id,)
    ).fetchone()

    if trip is None:
        return jsonify({"error": "Sorryyy! There is no trip :("}), 404
    
    destination = data.get("destination", trip["destination"])
    start_date = data.get("start_date", trip["start_date"])
    end_date = data.get("end_date", trip["end_date"])
    nr_people = data.get("nr_people", trip["nr_people"])

    if int(nr_people) <=0:
        return jsonify({"error": "We need at least one traveler"}), 400
    
    db.execute(
        """
        UPDATE Trips
        SET destination = ?, start_date = ?, end_date = ?, nr_people = ?
        WHERE trip_id = ?
        """, (destination, start_date, end_date, nr_people, trip_id)
    )

    db.commit()
    return jsonify({"message": "We have updated your trip! :*"}), 200

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id: int):
    """
    Delete a trip by its id. Return an error if the trip does not exist.
    """
    db = get_db()

    trip = db.execute(
        'SELECT * FROM Trips WHERE trip_id = ?', (trip_id,)
    ).fetchone()

    if trip is None:
        return jsonify({'error': 'There is no trip :('}), 404#
    
    db.execute(
        'DELETE FROM Itineraries WHERE trip_id = ?', (trip_id,)
    )
    
    db.execute(
        'DELETE FROM Trips WHERE trip_id = ?', (trip_id,)
    )

    db.commit()
    return jsonify({'message': 'Trip deleted successfully! '}), 200

