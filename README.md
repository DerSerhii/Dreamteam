# DREAM TEAM API

This project was completed as part of the **Wht.agency** test task.<br>
This is done using the **Django** and **Django REST** frameworks. <br>
**Postgres** database was used to store and work with data.<br>
**JSON Web Token (JWT)** is used for user authentication.

API documentation: http://127.0.0.1:8000/swagger/ (*start a test server*)
<hr>

## Description
Provided endpoints allow you to create closed memberships.
An example of such a membership in this project is the simplified IT structure of the company.

Each member has his own position in the company, which can change. Certain positions have a manager role.

Individual teams can be created within company. Only managers can create teams, add or remove members there.<br>
Within this project, teams can create positions such as PMs and Team Leads.

Membership is closed internally. Anyone can't register there. Only the manager can add a new member.
After transferring the username and password, the new member can enter the system.<br>
For the initial entrance, you need to create a django superuser. Superuser is granted the manager role by default.
You can create another manager with it or use it and the process will start.

There are members with positions that can only be added to one team, for example Trainee, Junior, Intermediate, etc. <br>
And there are positions that can be in different teams at the same time such as PM, DevOps, QA, etc.


<hr>

### Getting started
1. Download the code base on your local machine.
2. You may prefer to use virtual environment 
to separate the project's dependencies from other packages you have installed.

To install dependencies use `pip` or [poetry](https://python-poetry.org/):
```commandline
pip install -r requirements.txt
```
```commandline
poetry install
```

3. You must have [Postgres](https://www.postgresql.org/) database system installed. <br  >
Сreate a database, user and password according to the `DATABASES` in `settings.py` or change them to your own.
```commandline
sudo -u postgres psql
postgres=# create database dreamteam_db with encoding 'UTF8';
postgres=# create user dreamteam_user with password 'mypass';
postgres=# grant all on database dreamteam_db to dreamteam_user;
\c dreamteam_db
postgres=# grant all on schema public to dreamteam_user;
\q
```

4. The project requires some environment variables defined. To set up an environ variable do:

- Create `.env` file in the root of Django project.
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

- Paste the following entry in the `.env` file:
```
DATABASES_PASSWORD=some_password_of_your_postgres_database
DJANGO_SECRET_KEY=some_django_secret_key_see_below
```
|  Variable name	  | Variable description                                                                                                                                                                                                                                       |
|:----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|DJANGO_SECRET_KEY	| The secret key is required by Django security middleware. For the security reasons this can not be shared across the internet, and should be setup for each project individual instance separately. Here is a good service to get it: https://djecrety.ir/ |

5. Apply migrations to the database:
```commandline
python manage.py makemigrations
python manage.py migrate
```
6. Сreate a superuser:
```commandline
python manage.py createsuperuser
```
<hr>

### Launch project

1. To run the project do:
```
python manage.py runserver
```
2. Send a request using `curl`, [Postman](www.postman.com), etc.
