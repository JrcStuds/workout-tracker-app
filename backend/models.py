from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)
    exercises = db.relationship('Exercise', back_populates='workout', cascade='all, delete-orphan')

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.ForeignKey('workouts.id'))
    definition_id = db.Column(db.ForeignKey('exercise_definitions.id'))
    workout = db.relationship('Workout', back_populates='exercises')
    sets = db.relationship('Set', back_populates='exercise', cascade='all, delete-orphan')
    definition = db.relationship('ExerciseDefinition', back_populates='exercises')

class Set(db.Model):
    __tablename__ = 'sets'
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.ForeignKey('exercises.id'))
    set_number = db.Column(db.Integer)
    weight = db.Column(db.Float)
    reps = db.Column(db.Integer)
    rir = db.Column(db.Integer)
    exercise = db.relationship('Exercise', back_populates='sets')

class ExerciseDefinition(db.Model):
    __tablename__ = 'exercise_definitions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    primary = db.Column(db.String)
    secondary = db.Column(db.String)
    exercises = db.relationship('Exercise', back_populates='definition', cascade='all, delete-orphan')