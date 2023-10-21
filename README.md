# Minimal Amazon Clone in Django

(By Suyash Handa)

## Features

- User Authentication
- Product Listing
- Product Detail
- Cart
- Admin Panel
- Checkout

## Installation

- Clone the repository
- Create a virtual environment using `python -m venv env`
- Install the requirements using `pip install -r requirements.txt`
- Run the migration commands
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
- Create a superuser using `python manage.py createsuperuser`
- Run the server using `python manage.py runserver`

For a better understanding of the project, please try creating a few products from the admin panel at `localhost:8000/admin` and then try using the application.
