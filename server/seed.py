from app import app, db
from models import Workout, Exercise, WorkoutExercise

def seed_database():
    with app.app_context():
        print("Clearing database...")
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()

        print("Creating Sample Exercises...")
        exercise1 = Exercise(name="Push-ups", description="A basic upper body exercise.")
        exercise2 = Exercise(name="Squats", description="A basic lower body exercise.")
        db.session.add_all([exercise1, exercise2])
        db.session.commit()

        print("Creating Sample Workouts...")
        workout1 = Workout(name="Morning Routine", description="A quick morning workout.")
        workout2 = Workout(name="Evening Routine", description="A relaxing evening workout.")
        db.session.add_all([workout1, workout2])
        db.session.commit()

        print("Creating Sample Workout Exercises...")
        workout_exercise1 = WorkoutExercise(workout_id=workout1.id, exercise_id=exercise1.id, reps=10, sets=3)
        workout_exercise2 = WorkoutExercise(workout_id=workout1.id, exercise_id=exercise2.id, reps=15, sets=3)
        workout_exercise3 = WorkoutExercise(workout_id=workout2.id, exercise_id=exercise1.id, reps=5, sets=2)
        db.session.add_all([workout_exercise1, workout_exercise2, workout_exercise3])
        db.session.commit()

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully.")