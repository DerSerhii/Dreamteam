# DREAM TEAM API

This project is made as part of a test task.
This is done using the [Django](https://www.djangoproject.com/)
and [Django REST](https://www.django-rest-framework.org/) frameworks.

### Getting started
Download the code base on your local machine. You may prefer to use virtual environment 
to separate the project's dependencies from other packages you have installed.

To install dependencies use `pip` or [poetry](https://python-poetry.org/):
```commandline
pip install -r requirements.txt
```
```commandline
poetry install
```
After downloading the project, set the required environment variables.
Refer the table in *Environment variables* section for more information.

#### Environment variables
The project requires some environment variables defined. To set up an environ variable do:
1. Create `.env` file in the root of Django project.
```
.
├── dreamteam_project
│   ├── api
│   │   └── __init__.py
│   ├── dreamteam_project
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── .env               <-- CREATE HERE
│   └── manage.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt

```
2. Paste the following entry in the `.env` file:
```
DATABASES_PASSWORD=some_password_of_your_postgres_database
DJANGO_SECRET_KEY=some_django_secret_key_see_below
```
|  Variable name	  | Variable description                                                                                                                                                                                                                                       |
|:----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|DJANGO_SECRET_KEY	| The secret key is required by Django security middleware. For the security reasons this can not be shared across the internet, and should be setup for each project individual instance separately. Here is a good service to get it: https://djecrety.ir/ |

### Launch of the project

To run the project do:
```
python manage.py runserver
```

Send a request using `curl`, `Postman`, etc.