
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.config import Config
from server.models import db, Workout, Exercise, WorkoutExercise
from server.schemas import (
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


def get_request_data():
    """Require a JSON object in the request body."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValidationError({
            "_schema": ["Request body must be a JSON object."]
        })

    return data


def error_response(message, status_code):
    """Return a consistent JSON error response."""
    return jsonify({"error": message}), status_code


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error_response("Workout not found.", 404)

    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(get_request_data())
        workout = Workout(**data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response(
            "Workout data violates a database constraint.",
            400,
        )


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error_response("Workout not found.", 404)

    try:
        db.session.delete(workout)
        db.session.commit()
        return "", 204

    except IntegrityError:
        db.session.rollback()
        return error_response("Could not delete workout.", 409)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error_response("Exercise not found.", 404)

    result = exercise_schema.dump(exercise)

    result["workouts"] = [
        {
            "id": association.workout.id,
            "name": association.workout.name,
            "description": association.workout.description,
            "reps": association.reps,
            "sets": association.sets,
            "duration_minutes": association.duration_minutes,
        }
        for association in exercise.workout_exercises
    ]

    return jsonify(result), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(get_request_data())
        exercise = Exercise(**data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response(
            "Exercise data violates a database constraint.",
            400,
        )


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error_response("Exercise not found.", 404)

    try:
        db.session.delete(exercise)
        db.session.commit()
        return "", 204

    except IntegrityError:
        db.session.rollback()
        return error_response("Could not delete exercise.", 409)


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return error_response("Workout not found.", 404)

    if exercise is None:
        return error_response("Exercise not found.", 404)

    try:
        data = workout_exercise_schema.load(get_request_data())

        # IDs are taken from the URL, not the request body.
        data.pop("workout_id", None)
        data.pop("exercise_id", None)

        association = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            **data,
        )

        db.session.add(association)
        db.session.commit()

        return jsonify(workout_exercise_schema.dump(association)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response(
            "The workout-exercise association violates a database constraint.",
            409,
        )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
