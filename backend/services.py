from sqlalchemy import desc
from .database import Session
from .models import *


# --- CREATE ---

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
                        "weight": 60.0,
                        "reps": 10,
                        "rir": 1
                    },
                    ...
                ]
            },
            ...
        ]
    }
}
"""
def add_workout(data):
    with Session() as session:
        # create workout_obj with date
        workout_obj = Workout(date=data['workout']['date'])
        session.add(workout_obj)

        # loop through exercises in data and create an exercise obj
        for exercise in data['workout']['exercises']:
            definition_obj = session.query(ExerciseDefinition).filter_by(name=exercise['name']).first()
            exercise_obj = Exercise(
                workout = workout_obj,
                definition = definition_obj
            )
            session.add(exercise_obj)

            # loop through sets in current exercise in data and create obj
            for i, set in enumerate(exercise['sets']):
                set_obj = Set(
                    set_number = i + 1,
                    weight = set['weight'],
                    reps = set['reps'],
                    rir = set['rir'],
                    exercise = exercise_obj
                )
                session.add(set_obj)
        
        session.add(workout_obj)
        session.commit()


# input data format:
"""
{
    "name": "Bench Press",
    "primary": "chest",
    "secondary: "tricep,front_delt"
}
"""
def add_exercise_definition(data):
    with Session() as session:
        definition_obj = ExerciseDefinition(
            name = data['name'],
            primary = data['primary'],
            secondary = data['secondary']
        )
        session.add(definition_obj)
        session.commit()


# --- READ ---

# return data format:
"""
{
    "workouts": [
        {
            "date": "2025-01-02",
            "exercises": [
                "exercise 1",
                "exercise 2",
                ...
            ]
        },
        ...
    ]
}
"""
def get_workouts_overview():
    with Session() as session:
        result = []

        workouts = session.query(Workout).order_by(desc(Workout.date)).all()
        for workout in workouts:
            result.append({
                'date': workout.date,
                'exercises': [
                    exercise.definition.name for exercise in workout.exercises
                ]
            })
        
        return ({'workouts': result})


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
                    },
                    ...
                ]
            },
            ...
        ]
    }
}
"""
def get_workout(date):
    with Session() as session:
        workout = session.query(Workout).filter_by(date=date).first()

        result = {
            'workout': {
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
        }

        return result


# return data format:
"""
{
    "exercises": [
        "Bench Press",
        "Lat Pulldown",
        ...
    ]
}
"""
def get_exercise_definitions():
    with Session() as session:
        exercises = session.query(ExerciseDefinition).order_by(ExerciseDefinition.name).all()

        result = {
            'exercises': [
                exercise.name for exercise in exercises
            ]
        }

        return result


# --- UPDATE ---

# input data format:
"""
{
    "workout": {
        "old_date": "2025-01-01",
        "new_date": "2025-01-02",
        "exercises": [
            {
                "name": "Bench Press",
                "sets": [
                    {
                        "weight": 60,
                        "reps": 10,
                        "rir": 1
                    },
                    ...
                ]
            },
            ...
        ]
    }
}
"""
def edit_workout(data):
    delete_workout(date=data['workout']['old_date'])

    new_data = {
        'workout': {
            'date': data['workout']['new_date'],
            'exercises': data['workout']['exercises']
        }
    }

    add_workout(data=new_data)


# --- DELETE ---

def delete_workout(date):
    with Session() as session:
        workout = session.query(Workout).filter_by(date=date).first()
        session.delete(workout)
        session.commit()