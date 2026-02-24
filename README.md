## Event Management System with Web UI and REST API

This project is a Django-based event management system that includes a REST API backend, a functional web UI (Django templates), recurring events support, and a calendar view (FullCalendar.js) showing all occurrences.

## Software Requirements
- Python 3.10 or higher
- PostgreSQL 15 (or use Docker)
- Redis (for Celery task queue)

## Setup Instructions

### Option A: Local development
1. Clone the repository:
   ```
   git clone https://github.com/divyesh3489/Task_manangement
   cd Event-Management
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   use ".\venv\Scripts\activate" on Windows or "source ./venv/bin/activate" on macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure environment (PostgreSQL and Redis). Then apply migrations:
   ```
   cd event_manager
   python manage.py migrate
   ```
5. (Optional) Create a superuser:
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```
7. Access the application:
   - Web UI: `http://localhost:8000/`
   - Admin: `http://localhost:8000/admin/`

### Option B: Docker
1. From the project root:
   ```
   docker-compose up --build
   ```
2. The app runs at `http://localhost:8000/`. Migrations run automatically.

## API Endpoint Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
All event/recurrence/occurrence endpoints require a valid JWT. Obtain tokens via the user endpoints below.

### User Endpoints
- `POST /users/register/` : Register a new user
    - `Request Body`:
        - `email`: User email (string, required)
        - `password`: Password (string, required)

- `POST /users/login/` : Obtain JWT access and refresh tokens
    - `Request Body`:
        - `email`: User email
        - `password`: Password
    - Returns: `access`, `refresh` tokens

- `POST /users/refresh/` : Refresh access token
    - `Request Body`:
        - `refresh`: Refresh token

- `POST /users/logout/` : Blacklist refresh token (logout)
    - `Request Body`:
        - `refresh`: Refresh token to blacklist

- `GET /users/me/` : Get current user (requires authentication)
    - Headers: `Authorization: Bearer <access_token>`

### Event Endpoints
- `GET /events/` : List all events for the authenticated user
    - Returns list of events (with optional recurrence info)

- `GET /events/{event_id}/` : Retrieve an event by ID
    - `Path Parameters`:
        - `event_id`: UUID of the event

- `POST /events/` : Create a new event
    - `Request Body`:
        - `title`: Title of the event (string, required)
        - `description`: Description (string, optional)
        - `start_date`: Start datetime (ISO format, required)
        - `end_date`: End datetime (ISO format, required)
        - `recurrence`: Optional object with:
            - `frequency`: One of `daily`, `weekly`, `monthly`
            - `end_date`: End datetime for recurrence (optional)
            - `count`: Number of occurrences (optional; use either `end_date` or `count`, not both)

- `PUT /events/{event_id}/` : Update an event by ID
    - `Path Parameters`:
        - `event_id`: UUID of the event
    - `Request Body`: Same as POST (title, description, start_date, end_date, recurrence)

- `DELETE /events/{event_id}/` : Delete an event by ID
    - `Path Parameters`:
        - `event_id`: UUID of the event

### Recurrence Endpoints
- `GET /recurrences/` : List recurrences (via events)
- `GET /recurrences/{recurrence_id}/` : Retrieve a recurrence by ID
    - `Path Parameters`:
        - `recurrence_id`: UUID of the recurrence
- `PUT /recurrences/{recurrence_id}/` : Update a recurrence by ID
    - `Request Body`:
        - `frequency`: daily, weekly, monthly
        - `end_date`: optional
        - `count`: optional
- `DELETE /recurrences/{recurrence_id}/` : Delete a recurrence by ID

### Event Occurrence Endpoints
- `GET /event-occurrences/` : List event occurrences for the authenticated user
    - `Query Parameters`:
        - `start_date`: Filter occurrences from this date (ISO format, optional)
- `GET /event-occurrences/{occurrence_id}/` : Retrieve an event occurrence by ID
    - `Path Parameters`:
        - `occurrence_id`: UUID of the occurrence

## Web UI (Frontend) Routes

- `/` : Event list
- `/events/new/` : Create/edit event form
- `/events/calendar/` : Calendar view (FullCalendar.js, month view, all occurrences)
- `/register/` : User registration page

## Features

- **Event CRUD**: Create, read, update, delete events via API and web UI
- **Recurring events**: Daily, weekly, or monthly with either end date or occurrence count
- **Calendar view**: Month view with all occurrences; click event for details
- **Authentication**: JWT (login, refresh, logout) and user registration
- **Background tasks**: Celery + Redis for generating recurring occurrences

## Assumptions Made

- The API uses PostgreSQL for data persistence (configurable via Django settings).
- Events and recurrences are scoped to the authenticated user (`created_by`).
- Recurrence requires either `end_date` or `count`; both cannot be set.
- Occurrences are generated asynchronously via Celery after event/recurrence create or update.
- All event/recurrence/occurrence list and detail endpoints require a valid JWT in the `Authorization` header.
- Timestamps are stored and returned in UTC/ISO format.

## Requirements.txt

```
django==5.0.1
djangorestframework==3.15.2
psycopg2==2.9.10
djangorestframework-simplejwt==5.4.0
django-cors-headers==4.5.0
celery==5.3.0
redis==5.0.0
```
