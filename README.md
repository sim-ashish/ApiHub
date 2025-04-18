# ApiHub README

ApiHub is a Django-based project designed to provide a platform for users to create, manage, and interact with APIs. It is built with Django Rest Framework (DRF) and offers several features such as custom APIs, mock APIs, background task processing with Celery, and rate-limiting mechanisms. Additionally, it integrates caching via Redis and utilizes PostgreSQL as its database.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [URL Structure](#url-structure)
- [Throttling and Rate Limits](#throttling-and-rate-limits)
- [Authentication and Authorization](#authentication-and-authorization)
- [Task Management with Celery](#task-management-with-celery)
- [Caching with Redis](#caching-with-redis)
- [Database Setup (PostgreSQL)](#database-setup-postgresql)
- [Middleware](#middleware)


---

## Features

- **Playground APIs**: Interactive environment to test API endpoints.
- **Custom APIs**: Users can create custom APIs and define their data structures.
- **Mock APIs**: Mock different API responses for testing or simulation.
- **Throttling**: Implements rate-limiting to control traffic to the APIs:
  - Unauthenticated users: 30 requests per minute.
  - Authenticated users: 80 requests per minute.
  - Subscribers: 1000 requests per minute.
- **Authentication**: Supports session-based authentication for the frontend and JWT for API access.
- **Permissions**: Default permission class is `IsAuthenticatedOrReadOnly`, ensuring authenticated users have full access and unauthenticated users can only read data.
- **Background Task Processing**: Integrated with Celery to handle background tasks, such as sending emails.
- **Scheduled Tasks**: Uses Celery Beat to schedule periodic tasks.
- **Redis Caching**: Caching of frequently accessed data to improve API performance.
- **PostgreSQL Database**: Relational database system for data storage.
- **Frontend Integration**: DRF templated views for easy integration with frontend applications.

---

## Getting Started

Follow these steps to set up and run ApiHub locally:

### 1. Replace your credentials
Replace you email, database credentials in the .env file, also do redis config according to you
```bash
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email'
EMAIL_HOST_PASSWORD = 'you-password'
---------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
---------------------------------------------------------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME' : 'dq9aasttj',
    'API_KEY' : os.environ.get('API_KEY'),
    'API_SECRET'  :os.environ.get('API_SECRET')    
}
```

### 2. Create a Virtual Environment
First, create a Python virtual environment to isolate dependencies:
```bash
python -m venv venv
```

### 3. Installing Dependencies
Install the required Python packages from requirements.txt:
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
Make the necessary database migrations:
```bash
python manage.py makemigrations
```

### 5. Apply Migrations
Apply the migrations to set up the database:
```bash
python manage.py migrate
```

### 6. Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```

### 7. Start Celery Worker
Celery is used for background task processing. Start the Celery worker:
```bash
celery -A ApiHub worker -l info
```

### 8. Start Celery Beat
Celery Beat is used for scheduling periodic tasks. Start Celery Beat:
```bash
celery -A ApiHub beat -l info
```
---

## URL Structure

The project exposes several key API endpoints. Below is the list of primary URL patterns:

### User Management (`/user/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/user/` |	List all users
|POST |	`/user/` |	Create a new user
|GET |	`/user/<id>/` |	Retrieve a specific user
|PUT |	`/user/<id>/` |	Update a specific user
|DELETE |	`/user/<id>/`	| Delete a specific user

### Post Management (`/post/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/post/` |	List all posts
|POST |	`/post/` |	Create a new post
|GET |	`/post/<id>/` |	Retrieve a specific post
|PUT |	`/post/<id>/` |	Update a specific post
|DELETE |	`/post/<id>/` |	Delete a specific post

### Food Items (`/food-item/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/food-item/`	|List all food items
|POST |	`/food-item/`	|Create a new food item
|GET |	`/food-item/<id>/`	|Retrieve a specific food item
|PUT |	`/food-item/<id>/`	|Update a specific food item
|DELETE |	`/food-item/<id>/`	|Delete a specific food item

### Food Category (`/food-category/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/food-category/`	|List all food categories

### Food Orders (`/food-order/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/food-order/`	|List all food orders
|POST |	`/food-order/`	|Create a new food order
|GET |	`/food-order/<id>/`	|Retrieve a specific food order
|PUT |	`/food-order/<id>/`	|Update a specific food order
|DELETE |	`/food-order/<id>/`	|Delete a specific food order

### Clothing Management (`/clothes/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/clothes/`	|List all clothes
|POST |	`/clothes/`	|Create a new clothing item
|GET |	`/clothes/<id>/`	|Retrieve a specific clothing item
|PUT |	 `/clothes/<id>/`	|Update a specific clothing item
|DELETE	| `/clothes/<id>/`	|Delete a specific clothing item

### Fashion Category (`/fashion-category/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/fashion-category/`	|List all fashion categories

### Cloth Material (`/cloth-material/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/cloth-material/`	|List all cloth materials

### Custom APIs (`/custom-api/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/custom-api/`	|List all custom APIs
|POST |	`/custom-api/`	|Create a new custom API
|GET |	`/custom-api/<id>/`	|Retrieve a specific custom API
|PUT |	`/custom-api/<id>/`	|Update a specific custom API
|DELETE	| `/custom-api/<id>/`	|Delete a specific custom API

### Custom API Endpoints (`/endpoint/<slug:endpoint>/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/endpoint/<slug:endpoint>/`	|Retrieve a custom API endpoint
|PUT |	`/endpoint/<slug:endpoint>/`	|Update a custom API endpoint
|DELETE |	`/endpoint/<slug:endpoint>/`|Delete a custom API endpoint

### Mock APIs (/mock/)
| Method | Endpoint | Description |
|--------|----------|-------------|
|GET |	`/mock/`	|List all mock APIs
|POST |	`/mock/`	|Create a new mock API
|GET |	`/mock/<slug>/`	|Retrieve a specific mock API
|PUT |	`/mock/<slug>/`	|Update a specific mock API
|DELETE |	`/mock/<slug>/`	|Delete a specific mock API

### Authentication (/auth/)
| Method | Endpoint | Description |
|--------|----------|-------------|
|POST |	`/gettoken/`	|Obtain JWT token for authentication
|POST |	`/refreshtoken/`	|Refresh the JWT token
|POST |	`/token-verify/`	|Verify the JWT token



## Throttling and Rate Limits 
ApiHub implements API rate-limiting to prevent abuse and ensure fair usage:

|User Type | Rate Limit |
|----------|------------|
|Unauthenticated | 30 requests per day
|Authenticated | 80 requests per day
|Subscribers | 1000 requests per day

## Authentication and Authorization

ApiHub supports two types of authentication:

- Session Authentication: For frontend users accessing the API via browser sessions.

- JWT Authentication: For API users to authenticate via JSON Web Tokens (JWT).

The default permission class is IsAuthenticatedOrReadOnly, which means:

- Authenticated users can perform all operations.

- Unauthenticated users can only view data (read-only access).
