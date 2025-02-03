# 🛒 Django Shop - E-Commerce Platform

---

## 🛍️ Project Overview

Django Shop is a hands-on E-Commerce sneaker store project built as part of backend web development practice using Django. Crafted as a learning experience rather than a commercial product, but it showcases a rich set of features that reflect the developer's expertise and technical skills in building scalable web applications.

---

## 🛠️ Technologies

- **Back-end:** Python, Django, Django REST Framework (DRF), Celery, Redis, Gunicorn
- **Database & Caching:** PostgreSQL, Memcached
- **Testing:** Pytest, Flake8
- **Front-end:** HTML, CSS, Bootstrap, AJAX (for asynchronous requests)
- **Deployment & DevOps:** Docker, Docker-Compose, Nginx

---

## 🚀 Key Features

### 🔑 Authentication & Registration
- Registration via email or phone number
- Verification through email or SMS code
- Authorization via Bearer Token (API)
- User profile with editing capabilities

### 🛒 Shop Functionality
- Shopping cart with add/remove items, quantity adjustments, and clearing options
- Checkout process with personal and delivery details  
- Discount codes support
- Items page with filters (min/max price , category, name, currency), pagination, and search
- Wishlist feature with AJAX-based updates (using jQuery)
- REST API for CRUD operations on items, categories and feedbacks

### ✨ Additional Features
- Regular exchange rate updates via API from three local banks
- Dynamic product price updates based on current exchange rates
- Export and Import items list in CSV files
- Contact page with email support
- User feedbacks
- Background task execution using Celery and Redis
- Test coverage for core functionality

---

## ▶️ How to Run the Project?

The project runs using Docker-Compose.

1️⃣ **Clone the repository:**

   ```bash
   git clone https://github.com/SyvoLoTSkyi1/django_shop.git
   ```
   ```bash
   cd django_shop
   ```
2️⃣ **Create the .env file:**

Copy the `.env_example` file and rename it to `.env` using the following command:

   ```bash
   cp .env_example .env
   ```

Make sure to update the necessary environment variables in the `.env` file according to your setup, including database credentials, secret keys, and API keys.

3️⃣ **Start the containers:**
    
Make sure Docker is running on your machine and then use the following command:

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

P.S.Commands like ```python manage.py makemigrations```, ```python manage.py migrate``` and ```python manage.py collectstatic``` are not need, because project directory cotains ```entrypoint.sh``` file where these commands already used

---

## 📦 Demo-data in DB

After the project running if I'd like to see data in db follow next steps 😉

### 📥 Import Items via CSV

Admins can upload a CSV file to import items into the database using the built-in import feature.

1. Log in as a superuser or an admin.
2. Navigate to the **Import CSV** page in header or follow this link ```http://localhost/items/import_csv/```.
3. Upload ```items_import.csv``` file which is in project directory.
4. Submit the form to process the data.

Or you can upload your custom ```.csv``` file, but make sure it follows this format:

```
name,description,price,sku,category,image
Sneaker name 1,sneaker description 1,sneaker price 1,sneaker sku 1,sneaker category 1,sneaker/image/url/1
Sneaker name 2,sneaker description 2,sneaker price 2,sneaker sku 2,sneaker category 2,sneaker/image/url/2
```

P.S. This feature automatically creates categories if they don’t exist in db.

---

## ⭐ Give a Star!

If you liked the project, please give a star ;)

---

## 📜 License

This project is licensed under the MIT License.
