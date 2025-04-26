# 🛒 My Online Shop

## Project Description
Online Shop is an e-commerce platform that allows users to browse, purchase, and manage various products. This project includes all the essential features of an online store, such as:

- CRM panel for customer relationship management
- Rating and review system for each product and brand
- Q&A section for each product
- Warranty and after-sales service
- Discount coupon system
- JWT authentication for enhanced security
- Order process, final payment, and order tracking

## Features
- User registration and login with JWT
- User panel management (password change and profile updates)
- Order management and final payment
- Product and brand rating and review system
- Warranty and discount coupon management
- Q&A section for each product
- Track order shipping and delivery status

## Installation and Setup

To get started, first clone the project:

```bash
git clone https://github.com/Behnoushin/online_shop
cd online_shop


Then, create a virtual environment:
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate


Install the dependencies:
pip install -r requirements.txt

Run the project:
1. Migrate the database:
python manage.py migrate

2. Start the development server:
python manage.py runserver


Running with Docker:
To run the project with Docker, make sure Docker is installed and use the following command:
docker-compose up --build
This command will build and run the project in a Docker environment.


Crafted with ❤️ by Behnoushin (Behnoush Shahraeini)

