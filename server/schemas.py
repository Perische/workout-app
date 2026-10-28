
from flask_marshmallow import Marshmallow
from marshmallow import (
    ValidationError,
    fields,
    validates,
    validates_schema,
    validate,
)

ma = Marshmallow()


class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        include_fk = True
        load_instance = False

    exercise = fields.Nested(
        lambda: ExerciseSchema(exclude=("workout_exercises",)),
        dump_only=True,
    )

    @validates_schema
    def validate_positive_values(self, data, **kwargs):
        for field_name in ("reps", "sets", "duration_seconds"):
            value = data.get(field_name)
            if value is not None and value <= 0:
                raise ValidationError({
                    field_name: ["Must be a positive integer."]
                })

        if not any(
            data.get(field_name) is not None
            for field_name in ("reps", "sets", "duration_seconds")
        ):
            raise ValidationError(
                "Provide reps, sets, or duration_seconds."
            )


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = False

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema(exclude=("workout",)),
        many=True,
        dump_only=True,
    )

    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("Duration must be positive.")


class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = False

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError("Exercise category cannot be empty.")


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
