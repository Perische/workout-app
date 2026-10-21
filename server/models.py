from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Workout name cannot be empty")
        return value

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Exercise name cannot be empty")
        return value

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)
    
    workout = db.relationship('Workout', back_populates='exercises')
    exercise = db.relationship('Exercise')

    @validates('reps', 'sets', 'duration_minutes')
    def validate_positive_integer(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} must be a positive integer")
        return value
    