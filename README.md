# ShopKart Backend

## Overview
ShopKart Backend is a robust and scalable backend system for an e-commerce platform. It provides APIs for user authentication, product management, order processing.

## Features
- **User Authentication**: JWT-based authentication for secure user access.
- **Product Management**: CRUD operations for managing products.
- **Order Management**: Handling orders, payments, and order history.
- **Cart Management**: Adding, updating, and removing items from the cart.
- **Admin Panel**: Role-based access control for managing products and users.


## Tech Stack
- **Backend Framework**: Django Rest Framework (DRF)
- **Database**: MySQL
- **Authentication**: JWT Authentication

## Installation
### Prerequisites
- Python 3.13
- MySQL
- Virtual environment (Recommended)

### Steps to Set Up
1. **Clone the Repository**
   ```sh
   git clone https://github.com/Ajith-sav/backend_Shopcart.git
   cd backend_Shopcart
   ```

2. **Create a Virtual Environment & Activate It**
   ```sh
   python -m venv .venv
   .venv/bin/activate 
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file and add the necessary configurations:
   ```ini
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_database_url
   ````

5. **Run Migrations**
   ```sh
   python manage.py migrate
   ```

6. **Create a Superuser** (For Admin Access)
   ```sh
   python manage.py createsuperuser
   ```

7. **Start the Development Server**
   ```sh
   python manage.py runserver
   ```

## API Endpoints
### Authentication
- `POST /api/auth/register/` - User Registration
- `POST /api/auth/login/` - User Login
- `POST /api/auth/logout/` - User Logout
- `POST /api/auth/token/` - Generate new token

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Add a new product (Admin only)
- `GET /api/products/{id}/` - Retrieve a specific product
- `PUT /api/products/{id}/` - Update a product (Admin only)
- `DELETE /api/products/{id}/` - Delete a product (Admin only)

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Place an order
- `GET /api/orders/{id}/` - View order details


## License
This project is licensed under the MIT License.

