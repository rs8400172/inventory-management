# 📦 Inventory & Order Management System

A full-stack Inventory & Order Management System built using **React, Flask, PostgreSQL, and Docker**.

## 🚀 Features

* Product Management (CRUD)
* Customer Management (CRUD)
* Order Management
* Automatic Stock Reduction
* Low Stock Alerts
* Dashboard Statistics
* SKU & Email Uniqueness Validation
* Dockerized Deployment

## 🛠️ Tech Stack

**Frontend:** React, Vite, Material UI, Axios

**Backend:** Flask, SQLAlchemy, Pydantic

**Database:** PostgreSQL

**DevOps:** Docker, Docker Compose

## 📊 Business Rules

* Unique Product SKU
* Unique Customer Email
* No Negative Stock
* Prevent Orders with Insufficient Inventory
* Automatic Order Total Calculation
* Automatic Stock Updates

## 🚀 Run Locally

```bash
docker-compose up --build
```

### Access

* Frontend: http://localhost:3000
* Backend: http://localhost:8000

## 📌 Key Features

### Products

* Add, Update, Delete Products
* Inventory Tracking

### Customers

* Manage Customer Records
* Email Validation

### Orders

* Create Orders
* Multi-product Support
* Stock Validation

### Dashboard

* Total Products
* Total Customers
* Total Orders
* Low Stock Alerts

## 🏗️ Architecture

React Frontend → Flask API → PostgreSQL Database

All services are containerized using Docker and managed with Docker Compose.

## 👨‍💻 Author

**Ravindra Singh**

Full Stack Developer | Python | React | PostgreSQL | Docker
