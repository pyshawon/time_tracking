# Time Tracking Application

Multi-User and Multi-Project work time tracking application

## Installation

```bash
git clone git@github.com:pyshawon/time_tracking.git
cd time_tracking
virtualenv -p python3.9 env
source env/bin/activate
cd src
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

```

## Test

```bash
python manage.py test
```

## API Documentation
Swagger: http://127.0.0.1:8000/swagger/ \
Redoc: http://127.0.0.1:8000/redoc/


## License
[MIT](https://choosealicense.com/licenses/mit/)