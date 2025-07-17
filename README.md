[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
[![Django](https://img.shields.io/badge/Django-5.2-success)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Last Commit](https://img.shields.io/github/last-commit/PnEcrins/intrablog)](https://github.com/PnEcrins/intrablog/commits/main)
[![Issues](https://img.shields.io/github/issues/PnEcrins/intrablog)](https://github.com/PnEcrins/intrablog/issues)

<!-- [![Build Status](https://img.shields.io/github/actions/workflow/status/PnEcrins/intrablog/django.yml?branch=main)](https://github.com/PnEcrins/intrablog/actions) -->

# 📝 IntraBlog – A Django Blog Project

A blog platform built with Django and PostgreSQL.  
Includes users, authors, categories and post management.

---

## 🚀 Quick Setup

### 📦 Requirements

- Python 3.10+
- PostgreSQL
- pip or pipenv
- gettext installed on your machine

---

## ⚙️ Installation Guide

### 1. Clone the project

```bash
git clone https://github.com/PnEcrins/intrablog.git
cd intrablog
```

### 2. Create virtual environment

```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Make sure you have [`python-dotenv`](https://pypi.org/project/python-dotenv/) installed.

---

### 4. Set up environment variables and config file

1. Copy the example file:

   ```bash
   cp .env-sample .env
   cp  intraBlog/local_settings.py.sample intraBlog/local_settings.py
   ```

2. Edit `.env` and fill in your PostgreSQL credentials:
   ```ini
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_password
   SECRET_KEY=your_django_secret_key
   ```

---

### 5. Set up PostgreSQL database

Log in to PostgreSQL and create your database and user:

```sql
CREATE USER your_db_user WITH PASSWORD 'your_password';
CREATE DATABASE your_db_name OWNER <DB_USER> ;
```

---

### 6. Run migrations

```bash
python manage.py migrate
```

---

### 7. Create admin user

```bash
python manage.py createsuperuser
```

---

### 8. Run the server (dev)

```bash
python manage.py runserver
```

Then visit: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

### 9. Deploy in prod

Run this command in order to group all static files in one single place :

   python manage.py runserver

You must install a web server to deploy the application. Here is an example using Apache :

   apt install apache2
   a2enmod proxy
   a2enmod proxy_http

Create a conf in `/etc/apache2/sites-availables`


      <VirtualHost *:80>
         ServerName intrablog

         Alias "/static/" "/home/intranet/intraBlog/static/"
         <Directory "/home/intranet/intraBlog/static">
            Require all granted
         </Directory>


         <Location "/">
            ProxyPass http://127.0.0.1:8000/
            ProxyPassReverse http://127.0.0.1:8000/
            ProxyPreserveHost On
         </Location>

         <Location "/static">
            ProxyPass !
         </Location>
      </VirtualHost>


Change the local_settings.py parameters :

   ALLOWED_HOSTS = ["myhost"]
   CSRF_TRUSTED_ORIGINS = ["http://myhost"]


## 🛡 .env Security

⚠️ **Never commit your real `.env` file!**

Make sure `.env` is in `.gitignore` (already included).

---

## ✅ Features

- User registration & authentication
- Author & Category models
- Blog post CRUD
- Admin panel customization
- PostgreSQL support

---

## 🛠 Technologies

- Python 3.12.4
- Django 5.2
- Django Rest Framework
- PostgreSQL 16.8
- HTML/CSS (admin)
- python-dotenv for environment config

---

## 📁 Folder Structure

```
intrablog/
├── blog/             ← your app
├── intrablog/        ← settings, urls, wsgi
├── locale/           ← language locales
├── media/            ← your images and files (ignored)
├── env/              ← virtual environment (ignored)
├── .env              ← your local config (ignored)
├── .env-sample       ← template for developers
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧑‍💻 Contributing

Forks welcome! Open an issue or pull request if you'd like to collaborate.

---

## 📜 License

GPL-3.0 License.

---
