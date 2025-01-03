# E-commerce-product-management-system

An API for managing products, discounts, and product-related operations in an e-commerce system. This project is built using Django, Django REST Framework, and Swagger for API documentation.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [API Endpoints](#api-endpoints)
6. [Testing](#testing)
7. [License](#License)
8. [Contact](#contact)

## Introduction

This is a back-end API for an e-commerce platform built with Django and Django REST Framework. The API provides various functionalities like:

- Product management (CRUD)
- Discount management (CRUD)
- Swagger-based API documentation
- Apply discounts to products based on various criteria (percentage or fixed amount)

## Features

- **Product Management**: Create and retrieve products and product details.
  <img width="1180" alt="Screenshot 2025-01-03 at 05 22 08" src="https://github.com/user-attachments/assets/f4b83d3c-d2f2-4b6f-b352-3dc4e0717a2f" />
  <img width="823" alt="Screenshot 2025-01-03 at 05 22 31" src="https://github.com/user-attachments/assets/7f3ac8b1-afcd-4fb8-8170-57342b1c7f97" />

- **Discount Management**: Create and retrieve discount records.
  <img width="1213" alt="Screenshot 2025-01-03 at 05 34 28" src="https://github.com/user-attachments/assets/daef4e3b-c193-4c66-8857-238ba9dedd03" />

- **Discount Application**: Apply percentage or fixed discounts to product prices.
  <img width="1170" alt="Screenshot 2025-01-03 at 05 36 52" src="https://github.com/user-attachments/assets/b1de84f6-ef6a-42ac-942f-87b93608a434" />

- **Category Creation**: Create categories, Retrieve, Update and Delete categories
  <img width="1148" alt="Screenshot 2025-01-03 at 05 21 30" src="https://github.com/user-attachments/assets/f9e0a329-f120-43a2-8aee-923f2626ea9e" />

- **API Documentation**: Automatically generated Swagger documentation for easy interaction with the API.
  
  <img width="1238" alt="Screenshot 2025-01-03 at 05 53 34" src="https://github.com/user-attachments/assets/6227030f-e777-4c65-b7a8-04d504a3e36a" />



## Installation

### Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- Django 4.0 or higher
- Django REST Framework 3.12 or higher
- `django-rest-swagger` for API documentation

### Clone the Repository

Clone this repository to your local machine using:

```bash
git clone [https://github.com/codestron-name.git](https://github.com/Codestronomer/E-commerce-product-management-system.git
```

### Install Dependencies

Navigate into the project directory and install the dependencies

```bash
cd your-project-directory
pip install -r requirements.txt
```

### Database Setup

	1.	Ensure that you have a database set up (e.g., PostgreSQL, SQLite).
	2.	Run the following command to apply the migrations:
 
 ```bash
 python manage.py migrate
```

### Run the Development Server

To start the development server:

```
python manage.py runserver
```
The server will start at http://127.0.0.1:8000/.

### Configuration

The following settings can be configured in the settings.py file:
	•	Database Configuration: Set up your database settings (SQLite is used by default).
	•	Swagger Documentation: The API is documented using Swagger, which can be accessed at http://127.0.0.1:8000/swagger/.

## API Endpoints

### Product Endpoints

#### 1. Create a Product
- **URL**: `/api/products/`
- **Method**: `POST`

#### 2. Get All Products
-	**URL**: `/api/products/`
- **Method**: `GET`

### Discount Endpoints

#### 1. Create a Discount
- **URL**: `/api/discounts/`
- **Method**: `POST`

#### 2. Get all Discount
- **URL**: `/api/discounts/`
- **Method**: `GET`

#### 3. Apply Discount to Product
- **URL**: `/api/products/{product_id}/{discount_id}/`
- **Method**: `POST`

### Testing

To run the tests for this project:
	1.	Ensure you have a test database set up.
	2.	Run the following command to execute the test suite:

```bash
python manage.py test
```

### License

This project is licensed under the GNU License - see the LICENSE file for details.

### Contact

If you have any questions or need further information, feel free to reach out to me via the following methods:

- **Email**: [johnrumide@gmail.com](mailto:johnrumide@gmail.com)
- **GitHub**: [github.com/codestronomer](https://github.com/codestronomer)
I welcome any inquiries or suggestions you may have.

