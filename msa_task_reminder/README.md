# task reminder microservice


## overview

This microservice allows users to schedule, update, retrieve, and delete task reminders. It uses FastAPI for handling API requests, PostgreSQL for database storage, Celergy for background task scheduling, and Redis as the task broker.

## how to start the microservice

### 1. prerequisites
* install **Docker**, **PostgreSQL**, and **Redis**
* instal dependencies: <br />
  pip install fastapi pydantic celery redis uvicorn requests sqlalchemy psycopg2

### 2. start services
* start **PostgreSQL**: <br />
  docker start postgres-container
* start **Redis**: <br />
  docker start redis-container
* apply database migrations: <br />
  python -c "from taskScheduler import Base, engine; Base.metadata.create_all(bind=engine)"
* start **Celery** worker: <br />
  celery -A taskScheduler.celery worker --loglevel=info --pool=solo
* start **FastAPI**: <br />
  uvicorn taskScheduler:app --reload

## API endpoints

### 1. schedule a reminder
  * endpoint: POST /api/reminders
  * request body: <br />
    { <br />
      "task_id": 1, <br />
      "title": "Team Meeting", <br />
      "due_date": "2025-02-25", <br />
      "priority": "High", <br />
      "notify_time": "2025-02-24T10:00:00" <br />
    }
  * response: <br />
    { "status": "Reminder scheduled", "task_id": 1 }

### 2. update a reminder
  * endpoint: PUT /api/reminders/{task_id}
  * request body: <br />
    { <br />
      "task_id": 1, <br />
      "title": "Updated Meeting", <br />
      "due_date": "2025-02-26", <br />
      "priority": "Medium", <br />
      "notify_time": "2025-02-25T09:00:00" <br />
    }
  * response: <br />
    { "status": "Reminder updated", "task_id": 1 }

### 3. get all reminders
  * endpoint: GET /api/reminders
  * request body: <br />
    [ <br />
      > { <br />
        "title": "Updated Meeting", <br />
        "priority": "Medium", <br />
        "task_id": 1, <br />
        "id": 1, <br />
        "due_date": "2025-02-26", <br />
        "notify_time": "2025-02-25T09:00:00" <br />
      } <br />

    ] 
  * response: <br />
    { "status": "Reminder updated", "task_id": 1 }

### 4. delete a reminder
  * endpoint: DELETE /api/reminders/{task_id}
  * response: <br />
    { "status": "Reminder canceled", "task_id": 1 }

## UML sequence diagram
![uml_scheduler](uml_scheduler.png)
