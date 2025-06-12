# Mechanic Shop API

A full-featured RESTful API built using Flask to manage a mechanic shop’s operations, including customer records, service tickets, mechanics, and parts inventory. The project includes Swagger API documentation, token-based authentication, advanced querying, rate limiting, caching, and full unit testing.

## 🚀 Features

- 🔐 Token-based authentication for customers and optionally for mechanics
- 🧾 Full CRUD for Customers, Mechanics, Service Tickets, and Inventory Parts
- ⚙️ Many-to-many relationships between service tickets, mechanics, and parts
- 📄 Swagger documentation for all endpoints
- 📦 Caching and Rate Limiting with Flask-Caching and Flask-Limiter
- 🔬 Unit tests with Python `unittest` for each route
- 🛠️ Advanced querying and pagination
- 🌐 Hosted on Render with CI/CD via GitHub Actions

---

## 📁 Project Structure

mechanic_shop_api/
├── app/
│ ├── blueprints/
│ │ ├── customers/
│ │ ├── mechanics/
│ │ ├── service_tickets/
│ │ └── parts/
│ ├── models.py
│ ├── init.py
│ └── ...
├── tests/
│ ├── test_customers.py
│ ├── test_mechanics.py
│ ├── test_service_tickets.py
│ └── test_parts.py
├── swagger.yaml
├── flask_app.py
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 🔧 Setup and Installation


1. git clone https://github.com/blitzaced/mechanic_shop_api.git
2. cd mechanic_shop_api
3. python -m venv venv
4. source venv/bin/activate  # or venv\Scripts\activate on Windows
5. pip install -r requirements.txt

### Set up your .env file:

- SECRET_KEY=your_secret_key
- DATABASE_URL=your_postgres_uri


### Then run the app:

- flask --app flask_app run

---


## 🧪 Run Tests

- python -m unittest discover tests

---

## 📘 API Documentation
Visit http://mechanic-shop-api-4azh.onrender.com for interactive Swagger UI.

Each route includes:

- Path and method

- Request parameters and body (for POST/PUT)

- Response formats and examples

- Token security (where applicable)

---

## 🔑 Authentication
- Token-based authentication is implemented using python-jose.

- POST /login: Login route for customers

- @token_required: Decorator that protects secure routes

- GET /my-tickets: Returns tickets for logged-in customer

- Optional: separate token logic and decorator for mechanics.

---

## ⚡ Rate Limiting and Caching
- Rate limiting applied to sensitive routes with Flask-Limiter
- Response caching enabled on selected read routes via Flask-Caching

---

## 📦 Inventory
A dedicated blueprint and model to manage parts inventory:

- Many-to-many relationship with service tickets

- CRUD routes under /inventory

- Route to assign parts to tickets

---

## 🧪 Postman Collection
- A complete Postman collection is included in the repo for testing all routes.

---

## 🚀 Deployment (Render)
- Hosted on Render

- .env stores production secrets

- flask_app.py used as entry point

- Swagger host updated to live base URL

---

🔁 CI/CD
- GitHub Actions workflow in .github/workflows/main.yaml
- Steps include linting, testing, and deployment to Render
