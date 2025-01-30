# 🛒 Super Shop - E-Commerce Platform

&#x20;&#x20;

---

## 🛍️ Project Overview

Super Shop is a pet project of an E-Commerce sneaker store developed as part of backend web development training using Django. The project follows a project-based learning approach and is not intended for commercial use. However, it includes a comprehensive set of features that demonstrate the developer's knowledge and skills.

---

## 🛠️ Technologies

- **Back-end:** Python, Django, Django REST Framework (DRF), Celery, Redis, Gunicorn
- **Database & Caching:** PostgreSQL, Memcached
- **Testing:** Pytest, Flake8
- **Front-end:** HTML, CSS, Bootstrap, AJAX (for asynchronous requests)
- **Deployment & DevOps:** Docker, Docker-Compose, Nginx

---

## 🚀 Key Features

- **Authentication & Registration**
  - Registration via email or phone number
  - Verification through email or SMS code
  - Authorization via Bearer Token (API)
  - User profile with editing capabilities
- **Shop Functionality**
  - Shopping cart with add/remove items, quantity adjustments, and clearing options
  - Checkout process with personal details and address input
  - Discount codes support
  - Product page with filters (price, category, name, currency), pagination, and search
  - Wishlist feature with AJAX-based updates (using jQuery)
  - REST API for CRUD operations on items, categories, and feedbacks
- **Additional Features**
  - Regular exchange rate updates via API from three local banks
  - Dynamic product price updates based on current exchange rates
  - Contact page with email support
  - User feedbacks
  - Background task execution using Celery and Redis
  - Test coverage for core functionality

---

## 📦 How to Run the Project?

The project runs using Docker-Compose.

1️⃣ **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/super-shop.git
   ```
   ```bash
   cd super-shop
   ```
2️⃣ **Create the .env file:**

   Copy the `.env_example` file and rename it to `.env` using the following command:

   ```bash
   cp .env_example .env
   ```

   Make sure to update the necessary environment variables in the `.env` file according to your setup, including database credentials, secret keys, and API keys.

3️⃣ **Start the containers:**

   ```bash
   docker-compose up -d --build
   ```

4️⃣ **Create a superuser:**

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5️⃣ **The project will be available at:**

   ```
   http://localhost
   ```

---

## ⭐ Give a Star!

If you liked the project, please give a star ;)

---

## 📜 License

This project is licensed under the MIT License.
