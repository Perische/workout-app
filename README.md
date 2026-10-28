# Workout App

This is a Flask API for managing workouts and exercises. It allows users to create workouts, add exercises, view existing records, and delete them. Each exercise can be linked to a workout with details such as reps, sets, and duration.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- pytest

## Project Structure

```text
workout-app/
├── migrations/
├── server/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── tests/
│   └── test_app.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Getting Started

Clone the repository and move into the project directory:

```bash
git clone https://github.com/Perische/workout-app.git
cd workout-app
```

Install the dependencies:

```bash
pipenv install
```

## Database Setup

If migrations have not been initialized yet, run:

```bash
pipenv run flask --app server.app db init
```

Create and apply the database migration:

```bash
pipenv run flask --app server.app db migrate -m "Create workout tables"
pipenv run flask --app server.app db upgrade
```

To add sample data, run:

```bash
pipenv run python -m server.seed
```

## Running the App

Start the Flask server:

```bash
pipenv run flask --app server.app run --port 5555
```

The API will be available at `http://127.0.0.1:5555`.

## Available Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/workouts` | Get all workouts |
| GET | `/workouts/<workout_id>` | Get one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<workout_id>` | Delete a workout |
| GET | `/exercises` | Get all exercises |
| GET | `/exercises/<exercise_id>` | Get one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example Request

Create a workout by sending a `POST` request to `/workouts` with this JSON body:

```json
{
  "name": "Morning Workout",
  "description": "Full-body workout"
}
```

To create an exercise, send a `POST` request to `/exercises`:

```json
{
  "name": "Push-ups",
  "description": "Bodyweight exercise"
}
```

When adding an exercise to a workout, you can provide its reps, sets, and duration in minutes.

## Database Models

The app has three models:

- **Workout:** Stores the workout name and description.
- **Exercise:** Stores the exercise name and description.
- **WorkoutExercise:** Links workouts and exercises and stores reps, sets, and duration.

## Running Tests

Run the tests with:

```bash
pipenv run pytest -v
```

The tests check the API endpoints and how the app responds when a workout or exercise cannot be found.
