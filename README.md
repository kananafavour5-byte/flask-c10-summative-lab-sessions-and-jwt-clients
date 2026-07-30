# Task Manager API

A Flask RESTful API for managing personal tasks with secure session-based authentication. Users can register, log in, and manage their own tasks while ensuring that each user only has access to their own data.

## Repository

GitHub: https://github.com/kananafavour5-byte/flask-c10-summative-lab-sessions-and-jwt-clients

---

## Features

- User registration and login
- Session-based authentication using Flask-Session
- Secure password hashing with Flask-Bcrypt
- Create, Read, Update, and Delete (CRUD) tasks
- User-specific task ownership
- Protected API routes
- Task pagination
- Database migrations using Flask-Migrate
- Seed script for populating sample data

---

## Technologies Used

- Python 3
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Flask Session
- Flask Bcrypt
- Marshmallow
- SQLite
- Faker

---

## Project Structure

```text
flask-c10-summative-lab-sessions-and-jwt-clients/
│
├── client-with-jwt/
├── client-with-sessions/
├── server/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── migrations/
│   ├── instance/
│   ├── Pipfile
│   └── Pipfile.lock
│
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/kananafavour5-byte/flask-c10-summative-lab-sessions-and-jwt-clients.git
```

Navigate into the project:

```bash
cd flask-c10-summative-lab-sessions-and-jwt-clients/server
```

Install dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

---

## Database Setup

Run database migrations:

```bash
flask db upgrade
```

Populate the database with sample data:

```bash
python seed.py
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

The API runs at:

```
http://127.0.0.1:5555
```

---

# Authentication Endpoints

## Register

**POST** `/signup`

Registers a new user and starts a session.

Example request:

```json
{
  "username": "jane",
  "password": "12345",
  "password_confirmation": "12345"
}
```

---

## Login

**POST** `/login`

Logs an existing user into the application.

---

## Check Session

**GET** `/check_session`

Returns the currently authenticated user.

---

## Logout

**DELETE** `/logout`

Logs out the current user.

---

# Task Endpoints

All task routes require authentication.

## Get Tasks

**GET** `/tasks`

Supports pagination.

Example:

```
GET /tasks?page=1&per_page=10
```

---

## Create Task

**POST** `/tasks`

Example request:

```json
{
  "title": "Finish Flask Assignment",
  "description": "Complete the summative lab",
  "due_date": "2026-08-01"
}
```

---

## Update Task

**PATCH** `/tasks/<id>`

Updates a task owned by the authenticated user.

---

## Delete Task

**DELETE** `/tasks/<id>`

Deletes a task owned by the authenticated user.

---

## Pagination

The `/tasks` endpoint supports pagination using query parameters.

Example:

```
GET /tasks?page=1&per_page=5
```

Response includes:

- `tasks`
- `page`
- `per_page`
- `total`
- `pages`

---

## Sample Users

Running the seed script creates sample users and tasks for testing.

Example credentials:

| Username | Password |
|----------|----------|
| jane | 12345 |
| favour | password |

---

## Future Improvements

- Task categories
- Search and filtering
- Due date reminders
- Task priorities
- JWT authentication support
- Frontend integration

---

## Author

**Favour Kirema**

GitHub: https://github.com/kananafavour5-byte