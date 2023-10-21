# Minimal Amazon Clone in Django

(By Suyash Handa)

## Features

- User Authentication
- Product Listings
- Product Search (by Category and Product Name)
- Product Filter by Category
- Product Detail Pages
- Cart (with dynamic quantity update and delete)
- Admin Panel (for adding products and categories)
- Checkout (with subtotal)

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
