from .database import get_session
from .models import Workout, Exercise, Set, ExerciseDefinition
from datetime import date


# input data format (dict):
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
    session = get_session

    workout_obj = Workout(date=data['workout']['date'])
    session.add(workout_obj)

    for exercise in data['workout']['exercises']:
        definition_obj = session.query(ExerciseDefinition).filter_by(name=exercise['name']).first()
        exercise_obj = Exercise(
            workout = workout_obj,
            definition = definition_obj
        )
        session.add(exercise_obj)

        for i, set in enumerate(exercise['sets']):
            set_obj = Set(
                exercise = exercise_obj,
                set_number = i + 1,
                weight = set['weight'],
                reps = set['reps'],
                rir = set['rir']
            )
            session.add(set_obj)
    
    session.commit()
    session.close()

    return {'response': 'added_workout'}