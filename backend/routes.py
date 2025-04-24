from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from backend.models import db, Workout, Exercise, Set, ExerciseDefinition

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return "Workout Tracker App"

# --- outdated ---
@routes.route('/getworkouts', methods=['GET'])
def get_workouts():
    pass


@routes.route('/deleteworkout/<date>', methods=['DELETE'])
def delete_workout(date):
    # get workout by date
    workout = Workout.query.filter_by(date=date).first()

    # throw error if there is no workout on that date
    if not workout:
        return jsonify({"response": "workout does not exist"})

    # delete the workout
    db.session.delete(workout)

    db.session.commit()
    return jsonify({"response": "deleted workout"})


# input data format:
"""
{
    "workout": {
        "old_date": "2025-01-01",
        "new_date": "2025-01-02:,
        "exercises": [
            {
                "name": "Bench Press",
                "sets": [
                    {
                        "weight": 60,
                        "reps": 10,
                        "rir": 1
                    },
                ]
            },
        ]
    }
}
"""
@routes.route('/editworkout', methods=['POST'])
def edit_workout():
    data = request.get_json()['workout']

    # delete the workout from the database
    workout = Workout.query.filter_by(date=data['old_date']).first()
    db.session.delete(workout)
    db.session.commit()

    workout_obj = Workout(date=data['new_date'])
    db.session.add(workout_obj)

    for exercise in data['exercises']:
        exercise_obj = Exercise(
            workout = workout_obj,
            definition = ExerciseDefinition.query.filter_by(name=exercise['name']).first()
        )
        db.session.add(exercise_obj)

        for i, set in enumerate(exercise['sets']):
            set_obj = Set(
                set_number = i + 1,
                weight = set['weight'],
                reps = set['reps'],
                rir = set['rir'],
                exercise = exercise_obj
            )
            db.session.add(set_obj)

    db.session.commit()
    return jsonify({'response': 'added workout'})


# input data format:
"""
{
    "workout": {
        "date": "2025-01-01",
        "exercises": [
            {
                "name": "Bench Press",
                "sets": [
                    {
                        "weight": 60,
                        "reps": 10,
                        "rir": 1
                    },
                    {
                        "weight": 60,
                        "reps": 10,
                        "rir": 1
                    }
                ]
            }
        ]
    }
}
"""
@routes.route('/addworkout', methods=['POST'])
def add_workout():
    data = request.get_json()['workout']

    workout_obj = Workout(date=data['date'])
    db.session.add(workout_obj)

    for exercise in data['exercises']:
        exercise_obj = Exercise(
            workout = workout_obj,
            definition = ExerciseDefinition.query.filter_by(name=exercise['name']).first()
        )
        db.session.add(exercise_obj)

        for i, set in enumerate(exercise['sets']):
            set_obj = Set(
                set_number = i + 1,
                weight = set['weight'],
                reps = set['reps'],
                rir = set['rir'],
                exercise = exercise_obj
            )
            db.session.add(set_obj)

    db.session.commit()
    return jsonify({'response': 'added workout'})


# return data format:
"""
{
    "workouts": [
        {
            "date": "2025-01-02",
            "exercises": [
                "exercise 1",
                "exercise 2"
            ]
        },
        {
            "date": "2025-01-01",
            "exercises": [
                "exercise 1",
                "exercise 2"
            ]
        }
    ]
}
"""
@routes.route('/getworkoutsoverview', methods=['GET'])
def get_workouts_overview():
    result = []

    workouts = Workout.query.order_by(desc(Workout.date)).all()
    for workout in workouts:
        result.append({
            'date': workout.date,
            'exercises': [
                exercise.definition.name for exercise in workout.exercises
            ]
        })
    
    return jsonify({'workouts': result})


# return data format
"""
{
    "workout": {
        "date": "2025-01-01",
        "exercises": [
            {
                "name": "Bench Press"
                "sets": [
                    {
                        "set_number": 1,
                        "weight: 60.0,
                        "reps": 10,
                        "rir": 1
                    }
                ]
            }
        ]
    }
}
"""
@routes.route('/getworkout/<date>', methods=['GET'])
def get_workout(date):
    workout = Workout.query.filter_by(date=date).first()

    result = {
        'date': workout.date,
        'exercises': [
            {
                'name': exercise.definition.name,
                'sets': [
                    {
                        'set_number': set.set_number,
                        'weight': set.weight,
                        'reps': set.reps,
                        'rir': set.rir
                    }
                    for set in exercise.sets
                ]
            }
            for exercise in workout.exercises
        ]
    }
    
    return jsonify({'workout': result})


# input data format:
"""
{
    "name": "Bench Press",
    "primary": "chest",
    "secondary": "tricep,front_delt"
}
"""
@routes.route('/addexercisedefinition', methods=['POST'])
def add_exercise_definition():
    data = request.get_json()
    definition = ExerciseDefinition(
        name = data['name'],
        primary = data['primary'],
        secondary = data['secondary']
    )
    db.session.add(definition)
    db.session.commit()
    return jsonify({'response': 'added exercise definition'})


# return data format:
"""
{
    "exercises": [
        "Bench Press",
        "Lat Pulldown"
    ]
}
"""
@routes.route('/getexercisenames', methods=['GET'])
def get_exercise_names():
    result = []

    for exercise in ExerciseDefinition.query.order_by(ExerciseDefinition.name).all():
        result.append(exercise.name)
    
    return jsonify({'exercises': result})