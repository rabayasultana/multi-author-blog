# Multi-Author Blogging Platform

A Django-based Multi-Author Blogging Platform where readers can browse blog posts, like and comment on posts, and authors can create and manage their own blog posts.

---

## Features

- User Registration & Login
- Reader and Author Roles
- Author Dashboard
- Create, Edit and Delete Posts
- Categories and Tags
- Search Posts
- Filter by Category and Tag
- Like / Unlike Posts
- Comment System
- Author Public Profile
- View Count
- Pagination
- Django Admin Panel
- PostgreSQL Database
- Image Upload Support

---

# Technologies Used

- Python 3
- Django
- PostgreSQL
- HTML
- CSS
- JavaScript
- Pillow
- python-dotenv

---

# Project Setup

## 1. Clone the Repository

```bash
git clone https://github.com/rabayasultana/multi-author-blog.git

```

---

## 2. Create Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
```

### Windows

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Create PostgreSQL Database

Open PostgreSQL.

Create a database named:

```
blog_db
```

or any name you prefer.

---

## 6. Create .env File

Create a file named

```
.env
```

Copy the variables from

```
.env.example
```

Example:

```env
DJANGO_SECRET=your_secret_key

DB_NAME=blog_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 7. Run Database Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## 8. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts.

---

## 9. Run the Development Server

```bash
python manage.py runserver
```

Visit

```
http://127.0.0.1:8000/
```

Admin Panel

```
http://127.0.0.1:8000/admin/
```

---

# Database Backup & Restore

## Download the Database

The repository contains a PostgreSQL database backup file.



```
database/blog_db.dump
```

## Restore Custom Dump (.dump)

```bash
createdb blog_db
```

Restore:

```bash
pg_restore \
-d blog_db \
blog_db.dump
```

If using Windows:

```bash
pg_restore -U postgres -d blog_db blog_db.dump
```

---

## After Restoring

Update your `.env` file with your PostgreSQL credentials.

Then simply run

```bash
python manage.py runserver
```

No migration is required if the restored database already contains all tables.

---

# Media Files

Uploaded images are stored inside

```
media/
```

If media files are not included in the repository, create the folder:

```
media/posts/
```

or upload new images from the admin panel.

---

# Static Files

During development Django serves static files automatically.

For production:

```bash
python manage.py collectstatic
```

---

# Default User Roles

## Reader

- Register
- Login
- View posts
- Comment
- Like posts

---

## Author

An admin can promote a reader to an author from the Django Admin Panel.

Authors can

- Create posts
- Edit their own posts
- Delete their own posts
- View their dashboard

---

## Admin

Admin can

- Manage users
- Promote authors
- Manage categories
- Manage tags
- Manage posts
- Manage comments

---

# Important Notes

- Never commit the `.env` file.
- Use `.env.example` as a template.
- PostgreSQL must be running before starting the project.
- Pillow is required for image uploads.
- Images are uploaded inside the `media/` directory.

---

# Install Required Packages

```bash
pip install -r requirements.txt
```

---
