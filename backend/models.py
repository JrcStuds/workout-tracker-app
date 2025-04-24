from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    date = Column(String, unique=True)

    exercises = relationship('Exercise', back_populates='workout', cascade='all, delete-orphan')


class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    workout_id = Column(ForeignKey('workouts.id'))
    definition_id = Column(ForeignKey('exercise_definitions.id'))

    workout = relationship('Workout', back_populates='exercises')
    sets = relationship('Set', back_populates='exercise', cascade='all, delete-orphan')
    definition = relationship('ExerciseDefinition', back_populates='exercises')


class Set(Base):
    __tablename__ = 'sets'

    id = Column(Integer, primary_key=True)
    exercise_id = Column(ForeignKey('exercises.id'))
    set_number = Column(Integer)
    weight = Column(Float)
    reps = Column(Integer)
    rir = Column(Integer)

    exercise = relationship('Exercise', back_populates='sets')


class ExerciseDefinition(Base):
    __tablename__ = 'exercise_definitions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    primary = Column(String)
    secondary = Column(String)

    exercises = relationship('Exercise', back_populates='definition', cascade='all, delete-orphan')