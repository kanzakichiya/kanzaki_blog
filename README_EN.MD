# Kanzaki Chiya's Blog - Full-Stack Blog System

A modern full-stack blog system built from scratch with FastAPI (Backend) + Vue 3 (Frontend) + PostgreSQL. This project is fully containerized with Docker, Nginx, and Postgres for easy, high-performance, one-command deployment.

**[简体中文 (Chinese Version)](README.MD)**

---

### ✨ Features

* **Full Post Management**: Complete CRUD (Create, Read, Update, Delete) operations for articles.
* **Secure Authentication**: JWT-based user authentication (Register/Login) with protected admin routes and navigation guards.
* **Modern Editor**: Integrated **ByteMD** Markdown editor, supporting real-time preview, syntax highlighting, and secure image uploads.
* **Tag System**: Full-featured tag management (Create, Delete, Assign) and tag-based article filtering (e.g., `/tags/1`).
* **Containerized**: Fully containerized with Docker Compose for one-command deployment (`db`, `backend`, `frontend`).

### 🛠️ Tech Stack

* **Backend**:
    * Python 3.11
    * FastAPI (ASGI Framework)
    * SQLModel (ORM)
    * PostgreSQL (Database)
    * JWT (Authentication)
    * Bcrypt (Password Hashing)
* **Frontend**:
    * Vue 3 (Composition API)
    * Vue Router (Routing)
    * Pinia (State Management)
    * ByteMD (Markdown Editor)
* **Deployment**:
    * Docker & Docker Compose
    * Nginx (As a reverse proxy and static file server)

---

### 🚀 Getting Started (Production with Docker)

This is the easiest and recommended way to deploy the application on a server.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/my_blog_project.git](https://github.com/your-username/my_blog_project.git)
    cd my_blog_project
    ```

2.  **Create the Configuration File:**
    Create a file named `.env` in the root directory and copy the contents of `.env.example` (or the template below) into it. Fill in your desired passwords.

3.  **Build and Run:**
    ```bash
    docker-compose build
    docker-compose up -d
    ```

4.  **Done!**
    * The blog is now accessible at `http://localhost:5480` (or `http://your_server_ip:5480`).
    * The admin user you defined in `.env` is automatically created on first launch.

---

### ⚙️ Configuration (`.env` File)

Create a `.env` file in the project root. This file is **required** for Docker Compose.

```env
# --- Admin User Configuration (for first launch) ---
ADMIN_USER=admin
ADMIN_PASSWORD=your_secure_password_here
ADMIN_EMAIL=admin@example.com

# --- PostgreSQL Configuration ---
# (These are used by the 'db' service)
POSTGRES_USER=mybloguser
POSTGRES_PASSWORD=myblogpassword
POSTGRES_DB=myblogdb

# --- FastAPI Configuration ---
# (This is used by the 'backend' service)
# Note: 'db' is the service name from docker-compose.yml
DATABASE_URL=postgresql://mybloguser:myblogpassword@db/myblogdb
```

### 📄 License
This project is licensed under the MIT License. Copyright (c) 2025 Kanzaki Chiya.