from flask import flask, request,jsonify
from flask_migrate import Migrate
from config import Config
from models import db, workout, Exercise, WorkoutExercise
from schemas import (
    ma,
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@app.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_schema.dump(workout)), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json() or {}
    errors = workout_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_workout = workout_schema.load(data)
    db.session.add(new_workout)
    db.session.commit()
    return jsonify(workout_schema.dump(new_workout)), 201

@app.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404

    data = request.get_json() or {}
    errors = workout_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    workout.name = data.get('name', workout.name)
    workout.description = data.get('description', workout.description)
    db.session.commit()
    return jsonify(workout_schema.dump(workout)), 200

@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted successfully'}), 200

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

@app.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise_schema.dump(exercise)), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json() or {}
    errors = exercise_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_exercise = exercise_schema.load(data)
    db.session.add(new_exercise)
    db.session.commit()
    return jsonify(exercise_schema.dump(new_exercise)), 201

@app.route('/exercises/<int:exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404

    data = request.get_json() or {}
    errors = exercise_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    exercise.name = data.get('name', exercise.name)
    exercise.description = data.get('description', exercise.description)
    db.session.commit()
    return jsonify(exercise_schema.dump(exercise)), 200

@app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404

    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted successfully'}), 200

@app.routes('/workouts/<int:workout_id>/exercises', methods=['POST'])
def add_exercise_to_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404

    data = request.get_json() or {}
    exercise_id = data.get('exercise_id')
    if exercise_id is None:
        return jsonify({'error': 'Exercise ID is required'}), 400

    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404

    workout_exercise = WorkoutExercise(workout_id=workout.id, exercise_id=exercise.id)
    db.session.add(workout_exercise)
    db.session.commit()
    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

if __name__ == "__main__":
    app.run(debug=True)