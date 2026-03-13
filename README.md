# SiteSync

A job site management API built with FastAPI and PostgreSQL. Designed to help construction companies track job sites, manage tasks, and coordinate workers in real time.

## Live API
https://sitesync-wrjy.onrender.com/docs
```

## Live App
https://sitesync-app.netlify.app
```

## Features

- User registration and authentication with JWT tokens
- Create and manage job sites
- Add and track tasks per job site with status updates
- Protected endpoints — authentication required
- Auto-generated API documentation

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT with passlib password hashing
- **Deployment:** Railway

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL

### Installation

1. Clone the repository
```
   git clone https://github.com/Muamer-Pranjga/sitesync.git
   cd sitesync
```

2. Create a virtual environment
```
   python3 -m venv venv
   source venv/bin/activate
```

3. Install dependencies
```
   pip install -r requirements.txt
```

4. Create a PostgreSQL database named `sitesync` and update the connection string in `app/database.py`

5. Run the server
```
   uvicorn app.main:app --reload
```

6. Visit `http://127.0.0.1:8000/docs` to explore the API

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /register | Register a new user | No |
| POST | /login | Login and receive JWT token | No |
| GET | /job-sites | Get all job sites | Yes |
| POST | /job-sites | Create a job site | Yes |
| PUT | /job-sites/{id} | Update a job site | Yes |
| DELETE | /job-sites/{id} | Delete a job site | Yes |
| GET | /job-sites/{id}/tasks | Get tasks for a job site | Yes |
| POST | /job-sites/{id}/tasks | Create a task | Yes |
| PUT | /job-sites/{id}/tasks/{task_id} | Update a task | Yes |
| DELETE | /job-sites/{id}/tasks/{task_id} | Delete a task | Yes |

## Author

Muamer Pranjga — aspiring backend developer transitioning from construction management
```