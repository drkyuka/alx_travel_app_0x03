# 0. Django Project Setup with API Documentation and Database Configuration

## Objective

Set up the Django project with the necessary dependencies, configure the database, and add Swagger for API documentation.

## Instructions

## Create a Django Project:

- Set up a new Django project named `alx_travel_app`.
- Create an app within the project named `listings`.
- Install necessary packages, including `django`, `djangorestframework`, `django-cors-headers`, `celery`, `rabbitmq`, and `drf-yasg` for `Swagger` documentation.

## Configure Settings:

- In `settings.py`, configure the project for REST framework and CORS headers.
- Set up the database configuration to use `MYSQL`. Use environment variables for sensitive information such as database credentials. (Hint: Use the `django-environ` package to handle `.env` files).

## Add Swagger:

- Install `drf-yasg` for Swagger documentation.
- Configure `Swagger` to automatically document all APIs. The documentation should be available at `/swagger/`.

## Initialize Git Repository:

- Initialize a `Git` repository and make your initial commit with the project setup files.