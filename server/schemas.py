
from flask_marshmallow import Marshmallow
from marshmallow import (
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema,
)
from server.models import Exercise, Workout, WorkoutExercise
ma = Marshmallow()


class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        from server.models import Exercise

        model = Exercise
        load_instance = False

    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    category = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50),
    )
    equipment_needed = fields.Boolean(required=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Exercise name cannot be blank.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Exercise category cannot be blank.")


class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        from server.models import WorkoutExercise

        model = WorkoutExercise
        include_fk = True
        load_instance = False

    reps = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1),
    )
    sets = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1),
    )
    duration_seconds = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1),
    )

    exercise = fields.Nested(
        ExerciseSchema,
        dump_only=True,
    )

    @validates_schema
    def validate_measurements(self, data, **kwargs):
        measurement_fields = ("reps", "sets", "duration_seconds")

        if not any(data.get(field) is not None for field in measurement_fields):
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds."
            )


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        from server.models import Workout

        model = Workout
        load_instance = False

    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1),
    )
    notes = fields.String(
        required=False,
        allow_none=True,
    )

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema(exclude=("exercise",)),
        many=True,
        dump_only=True,
    )

    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("Workout duration must be positive.")


ExerciseSchema.workout_exercises = fields.Nested(
    WorkoutExerciseSchema(exclude=("exercise",)),
    many=True,
    dump_only=True,
)


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
