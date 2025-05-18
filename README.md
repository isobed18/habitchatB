# Habit Tracker - Social Habit Tracking Application

A social habit tracking application that allows users to track their habits, share progress with friends, and earn rewards through achievements.

## Features

- Habit tracking with time and count-based tracking
- Social features (friend system, photo sharing for habit verification)
- Achievement and reward system
- Customizable avatars
- Real-time chat
- Group challenges

## Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/isobed18/habitchatB.git
cd habitchatB
```

2. Create and activate virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

5. Create settings.py:
```bash
cp habit_tracker/settings_template.py habit_tracker/settings.py
```
Then edit `settings.py` and update the following:
- Generate a new SECRET_KEY
- Update ALLOWED_HOSTS if needed
- Configure your database settings

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Start the development server:
```bash
python manage.py runserver
```

9. Start Celery worker (in a separate terminal):
```bash
celery -A habit_tracker worker -l info
```

## Frontend Setup

This project has two frontend options:

1. Web Interface:
After starting the backend server, you can access the web interface at:
```
http://127.0.0.1:8000/
```

2. React Native Mobile App:
For the mobile app, please visit:
```
https://github.com/isobed18/habitchatF
```

## Important Commands and Configurations

### Server Configuration
- Start server on specific port:
```bash
python manage.py runserver 8000
```
- Allow all IPs in WiFi network:
```bash
python manage.py runserver 0.0.0.0:8000
```
- Configure ALLOWED_HOSTS in settings.py:
```python
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "your.local.ip"]  # Add your IP for LAN access. (CMD-> ipconfig-> LAN ADAPTER ipv4)
```

### Celery Commands
1. Start Celery Beat (Task Scheduler):
```bash
celery -A habit_tracker.my_celery beat --loglevel=debug --max-interval 5
```
Note: max-interval sets the refresh rate

2. Start Celery Worker (Windows specific):
```bash
celery -A habit_tracker.my_celery worker --loglevel=info --pool=solo
```
Note: --pool=solo is required for Windows

3. Use Database Scheduler:
```bash
celery -A habit_tracker.my_celery beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

4. Clean Celery Schedule:
```bash
rm celerybeat-schedule.*
redis-cli FLUSHALL
```

5. Call a specific task:
```bash
celery -A habit_tracker.my_celery call habit_tracker.tasks.add --args='[1, 2]'
```

### Time Synchronization (Windows)
If you need to change system time for testing:
1. Open Command Prompt as administrator
2. Set time: `time 00:00:00`
3. Resync time:
```bash
net stop w32time
w32tm /unregister
w32tm /register
net start w32time
w32tm /resync
```

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Technical Details and Troubleshooting

### Django and Channels Setup
1. Make sure Redis is running before starting the server:
```bash
# Windows
redis-server

# Linux/Mac
sudo service redis-server start
```

2. For WebSocket connections, ensure Daphne is running:
```bash
daphne -b 0.0.0.0 -p 8001 habit_tracker.asgi:application
```

3. If you get WebSocket connection errors:
- Check if Redis is running
- Verify ALLOWED_HOSTS includes your IP
- Ensure CORS settings are correct in settings.py

### Database Management
1. Create a new migration:
```bash
python manage.py makemigrations
```

2. Apply migrations:
```bash
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

### Celery and Task Management
1. Important Celery Configuration:
- Make sure Redis is running before starting Celery
- Windows requires `--pool=solo` parameter
- Database scheduler requires `django_celery_beat` in INSTALLED_APPS

2. Common Celery Issues:
- If tasks are not executing, check Redis connection
- For Windows users, ensure you're using `--pool=solo`
- If beat scheduler isn't working, try cleaning the schedule:
```bash
rm celerybeat-schedule.*
redis-cli FLUSHALL
```

### Development Environment
1. Virtual Environment:
- Always activate virtual environment before running commands
- If you get module not found errors, check if you're in the virtual environment

2. Environment Variables:
- Create a `.env` file in the root directory
- Required variables:
  ```
  DEBUG=True
  SECRET_KEY=your-secret-key
  DATABASE_URL=your-database-url
  REDIS_URL=redis://localhost:6379/0
  ```

3. Static Files:
- Collect static files:
```bash
python manage.py collectstatic
```
- Make sure STATIC_ROOT and STATIC_URL are configured in settings.py

### Testing
1. Run tests:
```bash
python manage.py test
```

2. Run specific app tests:
```bash
python manage.py test habits
python manage.py test friends
python manage.py test chat
```

### Production Deployment Notes
1. Security:
- Set DEBUG=False in production
- Use strong SECRET_KEY
- Configure proper ALLOWED_HOSTS
- Use HTTPS
- Set up proper CORS settings

2. Performance:
- Use a production-grade database (PostgreSQL recommended)
- Configure proper Redis settings
- Set up proper Celery worker processes
- Use a production-grade web server (Nginx recommended)

3. Monitoring:
- Set up proper logging
- Monitor Celery tasks
- Monitor Redis memory usage
- Set up error tracking

### Common Issues and Solutions
1. Database Issues:
- If migrations fail, try:
```bash
python manage.py migrate --fake
python manage.py migrate --fake-initial
```

2. Redis Connection Issues:
- Check if Redis is running
- Verify Redis URL in settings
- Check Redis port (default: 6379)

3. Celery Task Issues:
- Check Celery logs
- Verify task registration
- Check Redis connection
- Ensure proper task routing

4. WebSocket Issues:
- Check Daphne is running
- Verify Redis connection
- Check CORS settings
- Ensure proper routing configuration 
