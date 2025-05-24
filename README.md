# alx_travel_app

# About the Project

The `alx_travel_app` project is a real-world django application that serves as the foundation for a travel listing platform. This milestone focuses on setting up the initial project structure, configuring a robust database, and integrating tools to ensure API documentation and maintainable configurations. The aim is to equip learners with industry-standard best practices for starting and managing Django-based projects efficiently.

This milestone will teach you to set up a scalable backend, integrate `MySQL` for database management, and use Swagger for automated API documentation. These foundational steps are critical in preparing the application for future features and seamless team collaboration.

# Learning Objective
As a professional developer, this task will enable you to:

## Master Advanced Project Initialization:
- Learn to bootstrap Django projects with modular, production-ready configurations.
- Employ environment variable management for secure and scalable settings.

## Integrate Key Developer Tools:
- Set up and use `Swagger` (via `drf-yasg`) for API documentation.
- Implement CORS headers and MySQL configurations for robust API interactions.

## Collaborate Effectively Using Git:
- Structure your projects for team collaboration with a version-controlled setup.

## Adopt Industry Best Practices:
- Follow best practices in managing dependencies, database configurations, and application structure.

# Requirements
To successfully complete this milestone, ensure you meet the following prerequisites:
- Familiarity with `Django` and `Django REST Framework`.
- Knowledge of `MySQL` and database management.
- Understanding of version control using Git.
- A basic grasp of environment variable management using `django-environ`.

# Key Highlights

## Project Initialization:
- Create a Django project named `alx_travel_app`.
- Add an app named `listings` to encapsulate core functionalities.

## Dependency Management:
- Install essential packages:
    - `django`: Core framework for application development.
    - `djangorestframework`: REST API development.
    - `django-cors-headers`: Cross-Origin Resource Sharing setup.
    - `drf-yasg`: Swagger API documentation.
    - `celery` and `rabbitmq`: For future task queuing and background processes.

## Settings Configuration:
- Use `django-environ` to securely handle environment variables in `.env` files.
- Configure `MySQL` as the primary database, ensuring proper connection handling in `settings.py`.
- Set up REST framework and CORS headers for API support.

## Swagger Integration:
- Integrate Swagger for comprehensive API documentation.
- Ensure all APIs are automatically documented and accessible at `/swagger/`.

## Version Control and Submission:
- Initialize a Git repository and commit all project setup files.
- Push your code to a GitHub repository named `alx_travel_app` with the specified structure.
