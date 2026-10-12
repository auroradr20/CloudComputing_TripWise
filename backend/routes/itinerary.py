from flask import Blueprint, request, jsonify
from backend.db import get_db
from backend.services.opentripmap import get_places
from datetime import datetime
from backend.services.weather import get_weather_good
from backend.services.geodb import get_random_destination
import random
from datetime import datetime

itinerary_bp = Blueprint("itinerary",__name__)

ACTIVITY_COUNT_BY_INTENSITY = {
    'lazy' : 3,
    'normal' : 4,
    'busy' : 5
}

GROUP_TYPE_PREFERENCES = {
    'solo': ["museum", "culture", "sightseeing", "nature", "restaurant"],
    'couple': ["sightseeing", "restaurant", "culture", "park", "nature"],
    'friends': ["sport", "shopping", "restaurant", "sightseeing", "culture", "cinema"],
    'family': ["park", "museum", "nature", "sightseeing", "restaurant"]
}

all_activities =  ["restaurant", "museum", "culture", "cinema", 
                   "religion", "park", "nature", "hiking", 
                   "sport", "shopping", "sightseeing", "other"]
indoor_activities = ["restaurant","museum","culture","cinema","religion","shopping","sport"]

VIBE_PREFERENCES = {
    'chill': ["park", 'nature', 'restaurant', 'museum'],
    'adventure' : ['hiking', 'sport', 'nature', 'sightseeing'],
    'cultural' : ['museum', 'culture', 'religion', 'sightseeing'],
    'social' : ['restaurant', 'shopping', 'cinema', 'culture']
}

MAX_PER_ACTIVITY_TYPE = {
    'restaurant': 2,
    'museum': 2,
    'culture': 2,
    'cinema': 1,
    'religion': 2,
    'park': 2,
    'nature': 2,
    'hiking': 2,
    'sport': 2,
    'shopping': 2,
    'sightseeing': 2,
}

@itinerary_bp.route('/trips/<int:trip_id>/itinerary/generate', methods=['POST'])
def generate_itinerary(trip_id: int):
    """
    Generate one itinerary for one trip.
    """

    db = get_db()

    trip = db.execute(
        'SELECT * FROM Trips WHERE trip_id = ?', (trip_id,)
    ).fetchone()

    if trip is None:
        return jsonify({"error": "Sorryyy! There is no trip :("}), 404
    
    destination = trip['destination']
    places = get_places(destination)
    all_places = places.copy()

    try:
        weather_good = get_weather_good(destination)
    except Exception:
        weather_good = True

    data = request.get_json(silent=True) or {}

    activity_types = data.get('activity_types', [])
    day_intensity = data.get('day_intensity', 'normal')
    group_type = data.get('group_type')
    include_food = data.get('include_food', True)
    vibe = data.get('vibe')
    
    if not places:
        return jsonify({"error": "Sorryyy! We could not find any places for this destination :("}), 404

    if include_food is False:
        places = [p for p in places if p['activity_type'] != 'restaurant']

    if activity_types:
        places = [p for p in places if p['activity_type'] in activity_types] 

    if not weather_good:
        places = [p for p in places if p["activity_type"] in indoor_activities]

    if group_type in GROUP_TYPE_PREFERENCES:
        preferred_types = GROUP_TYPE_PREFERENCES[group_type]
        places.sort(key=lambda p: 0 if p['activity_type'] in preferred_types else 1)

    if vibe:
        if vibe not in VIBE_PREFERENCES:
            return jsonify({
                'error' : 'Vibe must be chill, adventure, cultural, or social'
            }), 400
        
        vibe_preferences = VIBE_PREFERENCES[vibe]

        places.sort(
            key=lambda place: (
                place['activity_type'] not in vibe_preferences,
                vibe_preferences.index(place['activity_type'])
                if place['activity_type'] in vibe_preferences
                else len(vibe_preferences)
            )
        )
        
    activity_limit = ACTIVITY_COUNT_BY_INTENSITY.get(day_intensity, 4) 

    start_date = datetime.strptime(str(trip['start_date']), "%Y-%m-%d")
    end_date = datetime.strptime(str(trip['end_date']), "%Y-%m-%d")
    number_of_days = (end_date - start_date).days + 1

    total_activity_limit = activity_limit * number_of_days

    selected_places = []
    activity_type_counts = {}
    selected_names = set()

    for place in places:
        activity_name = place['name'].strip().lower()
        activity_type = place['activity_type']

        if activity_name in selected_names:
            continue

        current_count = activity_type_counts.get(activity_type, 0)
        max_count = MAX_PER_ACTIVITY_TYPE.get(activity_type, activity_limit) * number_of_days

        if current_count < max_count:
            selected_places.append(place)
            selected_names.add(activity_name)
            activity_type_counts[activity_type] = current_count + 1

        if len(selected_places) >= total_activity_limit:
            break
            
    # If filters returned too few places, fill the remaining itinerary with other available places from the same destination.
    if len(selected_places) < total_activity_limit:
        for place in all_places:
            activity_name = place['name'].strip().lower()

            if activity_name in selected_names:
                continue

            if include_food is False and place['activity_type'] == 'restaurant':
                continue

            selected_places.append(place)
            selected_names.add(activity_name)

            if len(selected_places) >= total_activity_limit:
                break

    if not selected_places:
        return jsonify({"error": "Sorryyy! We could not find any activities to match your filters :("}), 404


    if not places:
        return jsonify({"error": "Sorryyy! We could not find any activities to match your filters :("}), 404
    

                    
    activity_nr = 1

    db.execute(
        "DELETE FROM Itineraries WHERE trip_id = ?", (trip_id,)
        )
    
    for index, p in enumerate(selected_places):
        day_number = (index // activity_limit) + 1
        activity_nr = (index % activity_limit) + 1
        
        db.execute(
        '''
        INSERT INTO Itineraries (trip_id, day_number, activity_nr, activity, address, activity_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',(trip_id, day_number, activity_nr, p['name'], p['address'], p['activity_type'], 'pending')
        )
        activity_nr += 1

    db.commit()
    return jsonify({'message': 'We created your itinerary! :)'}), 201


@itinerary_bp.route('/trips/<int:trip_id>/itinerary', methods=['GET'])
def get_itinerary(trip_id: int):
    """
    Retrieve all itinerary details for one trip.
    """

    db = get_db()

    trip = db.execute(
        'SELECT * FROM Trips WHERE trip_id = ?', (trip_id,)
    ).fetchone()

    if trip is None:
        return jsonify({"error": "Sorryyy! There is no trip :("}), 404
    
    status_filter = request.args.get('status')

    if status_filter:
        status_filter = status_filter.strip().lower()

        valid_statuses = ['pending', 'accepted', 'declined']

        if status_filter not in valid_statuses:
            return jsonify({'error' : 'Status must be pending, accepted, or declined'}), 400

        items = db.execute(
            """
            SELECT * FROM Itineraries 
            WHERE trip_id = ? AND status = ?
            ORDER BY day_number, activity_nr 
            """, (trip_id, status_filter)
        ).fetchall()

    else:
        items = db.execute(
            """
            SELECT * FROM Itineraries 
            WHERE trip_id = ?
            ORDER BY day_number, activity_nr 
            """, (trip_id,)
        ).fetchall()
    itinerary = []

    for i in items:
        itinerary.append({
            'itinerary_id': i['itinerary_id'],
            'trip_id': i['trip_id'],
            'day_number': i['day_number'],
            'activity_nr': i['activity_nr'],
            'activity': i['activity'],
            'address': i['address'],
            'activity_type': i['activity_type'],
            'status': i['status']
        })

    return jsonify({
        "trip_id": trip["trip_id"],
        "user_id": trip["user_id"],
        "destination": trip["destination"],
        "is_random": trip["is_random"],
        "itinerary": itinerary
    }), 200

@itinerary_bp.route('/trips/<int:trip_id>/itinerary/summary', methods=['GET'])
def get_itinerary_summary(trip_id:int):
    '''
    Get a summary of itinerary activity statuses for one trip.
    '''
    db = get_db()

    trip = db.execute(
        'SELECT * FROM Trips WHERE trip_id = ?', (trip_id,)
    ).fetchone()

    if trip is None:
        return jsonify({'error' : 'Sorryyyy! There is no trip :()'})
    
    total_activities = db.execute(
        '''
        SELECT COUNT(*) AS count
        FROM Itineraries
        WHERE trip_id = ?
        ''',
        (trip_id,)
    ).fetchone()['count']

    pending = db.execute(
        '''
        SELECT COUNT(*) AS count
        FROM Itineraries
        WHERE trip_id = ? AND status = ?
        ''',
        (trip_id, 'pending')
    ).fetchone()['count'] 

    accepted = db.execute(
        '''
        SELECT COUNT(*) AS count
        FROM Itineraries
        WHERE trip_id = ? AND status = ?
        ''',
        (trip_id, 'accepted')
    ).fetchone()['count'] 

    declined = db.execute(
        '''
        SELECT COUNT(*) AS count
        FROM Itineraries
        WHERE trip_id = ? AND status = ?
        ''',
        (trip_id, 'declined')
    ).fetchone()['count'] 

    return jsonify({
        'trip_id' : trip_id,
        'total_activities' : total_activities,
        'pending' : pending,
        'accepted' : accepted,
        'declined' : declined
    }), 200

@itinerary_bp.route('/itinerary/<int:itinerary_id>', methods=['PUT'])
def update_itinerary_status(itinerary_id: int):
    """
    Update the status of one activity in the itinerary.
    The status can be pending, accepted, or declined.
    """

    db = get_db()
    data = request.get_json() 

    if data is None:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'status' not in data:
        return jsonify({'error': 'Missing field: status'}), 400
    
    status = data['status']
    
    if status not in ['pending', 'accepted', 'declined']:
        return jsonify({'error': 'Status must be pending, accepted, or declined'}), 400
    
    itinerary_item = db.execute(
        'SELECT * FROM Itineraries WHERE itinerary_id = ?',
        (itinerary_id,)
    ).fetchone()

    if itinerary_item is None:
        return jsonify({'error': 'We could not find this activity :('}), 404
    
    db.execute(
        '''
        UPDATE Itineraries
        SET status = ?
        WHERE itinerary_id = ?
        ''', (status, itinerary_id)
    )

    db.commit()

    return jsonify({'message': 'We updated your activity successfully! Yeyyy!'}), 200

@itinerary_bp.route('/itinerary/<int:itinerary_id>/replace', methods=['POST'])
def replace_declined_activity(itinerary_id: int):
    '''
    Replace one declined activity from an itinerary with a new suggested activity.
    '''
    db = get_db()

    activity = db.execute(
        '''
        SELECT * FROM Itineraries
        WHERE itinerary_id = ?
        ''', (itinerary_id,)
    ).fetchone()

    if activity is None:
        return jsonify({'error' : 'We could not find this activity :('}), 404
    
    if activity['status'] != 'declined':
        return jsonify({
            'error': 'Only declined activities can be replaced'
        }), 400
    
    trip = db.execute(
        '''
        SELECT * FROM Trips
        WHERE trip_id = ?
        ''', (activity['trip_id'],)
    ).fetchone()

    if trip is None:
        return jsonify({'error' : 'Sorryyyy! There is no trip :('}), 404
    
    destination = trip['destination']
    places = get_places(destination)

    if not places:
        return jsonify({
            'error' : 'Sorryyyy! We could not find other activities :('
        }), 404
    
    existing_activities = db.execute(
        '''
        SELECT activity
        FROM Itineraries
        WHERE trip_id = ?
        ''',
        (activity['trip_id'],)
    ).fetchall()

    existing_names = [item['activity'].strip().lower() for item in existing_activities]

    replacement = None
    declined_activity_type = activity['activity_type']

    for place in places:
        place_name = place['name'].strip().lower()
        if (place_name not in existing_names and place['activity_type'] == declined_activity_type):
            replacement = place
            break

    if replacement is None:
        for place in places:
            place_name = place['name'].strip().lower()
            if place_name not in existing_names:
                replacement = place
                break

    if replacement is None:
        return jsonify({
            'error' : 'Sorryyyy! We could not find a new activity to replace this one :('
        }), 404
    
    db.execute(
        '''
        UPDATE Itineraries
        SET activity = ?, address = ?, activity_type = ?, status = ?
        Where itinerary_id = ?
        ''', (replacement['name'], replacement['address'], replacement['activity_type'], 'pending', itinerary_id)
    )

    db.commit()

    return jsonify({
        'message' : 'We successfully replaced the declined activity. Hope you enjoy!',
        'original_activity_type' : declined_activity_type,
        'replacement' : {'activity' :  replacement['name'],
                         'address' : replacement['address'],
                         'activity_type' : replacement['activity_type'],
                         'status' : 'pending'
                         }}), 200

@itinerary_bp.route('/itinerary/<int:itinerary_id>', methods=['DELETE'])
def delete_itinerary_item(itinerary_id: int):
    '''
    Delete one itinerary item by the itinerary's id.
    '''

    db = get_db()

    itinerary_item = db.execute(
        'SELECT * FROM Itineraries WHERE itinerary_id = ?', (itinerary_id,)
    ).fetchone()

    if itinerary_item is None:
        return jsonify({'error': 'We could not find this activity :('}), 404
    
    db.execute(
        'DELETE FROM Itineraries WHERE itinerary_id = ?', (itinerary_id,)
    )

    db.commit()

    return jsonify({'message': 'We deleted the activity. :*'}), 200



@itinerary_bp.route('/users/<int:user_id>/itinerary/random', methods=['POST'])
def random_itinerary(user_id: int):
    """
    Generate a random itinerary for an existing user.
    The only thing required is the user_id.
    """

    db = get_db()

    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()

    if user is None:
        return jsonify({"error": "Sorryyy! There is no user :("}), 404
    
    try:
        for attempt in range(5):
            destination = get_random_destination()
            places = get_places(destination, limit=30)

            if places:
                break

    except Exception as e:
        return jsonify({"error": "Sorryyy! We could not generate a random itinerary for you :("}), 500
    
    if not places:
        return jsonify({"error": "Sorryyy! We could not find any places for this destination :("}), 404
    
    random.shuffle(places)

    number_days = random.randint(1, 3)
    activities_day = random.randint(3, 5)

    total_activities = number_days * activities_day 
    selected_places = places[:total_activities]

    cursor = db.execute(
        """
        INSERT INTO Trips (user_id, destination, start_date, end_date, nr_people, is_random)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, destination, None, None, None, 1)
    )

    trip_id = cursor.lastrowid

    itinerary = []
    index = 0

    for day in range(1, number_days + 1):
        day_activities = []

        for activity_nr in range(1, activities_day + 1):
            if index >= len(selected_places):
                break

            place = selected_places[index]

            db.execute(
                """
                INSERT INTO Itineraries 
                (trip_id, day_number, activity_nr, activity, address, activity_type, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trip_id,
                    day,
                    activity_nr,
                    place['name'],
                    place['address'],
                    place['activity_type'],
                    'pending'
                )
            )

            day_activities.append({
                'activity_nr': activity_nr,
                'activity': place['name'],
                'address': place['address'],
                'activity_type': place['activity_type'],
                'status': 'pending'
            })  
            index += 1

        if day_activities:
            itinerary.append({
                'day_number': day,
                'activities': day_activities
            })
    
    db.commit()
    return jsonify({
        'message': 'We created your random itinerary! :)',
        'trip_id': trip_id,
        'user_id': user_id,
        'destination': destination,
        'number_days': number_days,
        'itinerary': itinerary
    }), 200
