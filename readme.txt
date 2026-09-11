# E-Commerce Management API

A lightweight, high-performance RESTful API service built with Python, FastAPI, and MySQL, featuring JWT authentication and transactional order processing.

---

## 🚀 Key Features

* **Authentication**: Secure registration, login, and JWT Bearer token authentication.
* **Product Management**: Public catalog browsing and protected admin CRUD operations.
* **Order Processing**: Real-time stock validation, automated inventory deduction, and unique order ID generation within a database transaction.
* **Payment Integration**: Secure payment handling with order state transitions (`PENDING_PAY` -> `PAID`).
* **Security**: Protection against Insecure Direct Object Reference (IDOR) by extracting identity directly from JWT tokens.

---

## 🛠️ Tech Stack

* **Framework**: FastAPI
* **Server**: Uvicorn
* **Database**: MySQL
* **DB Driver**: PyMySQL
* **Data Validation**: Pydantic v2
* **Authentication**: PyJWT + Passlib (Bcrypt)

---

## 📂 Project Structure

```text
├── api/          # API Route handlers (Endpoints)
├── service/      # Core business logic layer
├── DAO/          # Data Access Object layer (Raw SQL queries & transactions)
├── model/        # Pydantic data schemas & request/response validation
├── utils/        # JWT utilities, database connections, response formatters
└── main.py       # FastAPI application entry point