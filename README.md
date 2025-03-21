## HabitHub - Personal Habit Tracker
This app will help users track their habits and achievements. HabitHub makes it easy to set goals, track your progress.

## Features
- Habits and goals: add, modify and remove habits and goals.
- Calendar Tracking: Mark your habit completion directly in the calendar.
- User registration and authentication.
- Reminders: Set up custom notifications to keep you on track.
- Responsive Design & PWA: The site is fully responsive and works on various devices.

## Stack
- Backend: Python, Django
- Database: PostgreSQL
- Frontend: HTML, CSS, JavaScript
- Task Scheduling: Celery
- Visualization: Plotly
- Deployment: Docker, Nginx

## Installation
1. Clone the repository:
   ```
   https://github.com/AKamysheva/HabitHub
   cd habithub
   ```

2. Create a .env file
3. Build and Start the Containers:
   ```
   docker build -t habithub .
   docker-compose up -d
   ```
.env File Example
```
SECRET_KEY=mysecretkey
DEBUG=False
POSTGRES_DB=mydatabase
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_HOST_USER=apiemail
EMAIL_HOST_PASSWORD=passwordemail
```
   
