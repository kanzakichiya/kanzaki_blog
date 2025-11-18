<div align="center">
  <h1>Kanzaki Chiya's Blog - Full-Stack Blog System</h1>
  <p>
    A modern full-stack blog system built from scratch with FastAPI (Backend) + Vue 3 (Frontend) + PostgreSQL.
    <br />
    This project is fully containerized with Docker, Nginx, and Postgres for easy, high-performance, one-command deployment.
  </p>
  <p>
    <a href="README.MD"><strong>简体中文 (Chinese Version)</strong></a>
  </p>
</div>

---

### ✨ Features

* **Full Post Management**: Complete CRUD (Create, Read, Update, Delete) operations for articles.
* **Secure Authentication**: JWT-based user authentication (Register/Login) with protected admin routes and navigation guards.
* **Modern Editor**: Integrated **ByteMD** Markdown editor, supporting real-time preview, syntax highlighting, and secure image uploads.
* **Tag System**: Full-featured tag management (Create, Delete, Assign).
* **Dynamic Navigation**: Supports tag-based article filtering (e.g., `/tags/1`) and a full **Tag Index Page** (`/tags`).
* **Site Configuration**: Easily customize the **Blog Owner Name** and **Admin Account** via the `.env` file.
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
    * Docker & Docker Compose (v2)
    * Nginx (As a reverse proxy and static file server)

---

### 🚀 Getting Started (Production with Docker)

This is the easiest and recommended way to deploy the application on a server.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/kanzakichiya/kanzaki_blog.git](https://github.com/kanzakichiya/kanzaki_blog.git)
    cd kanzaki_blog
    ```

2.  **Create the Configuration File:**
    Create a file named `.env` in the root directory, copy the template below, and fill in your desired passwords and blog name.

3.  **Build and Run:**
    (Ensure you have Docker and Docker Compose v2 installed on your server)
    ```bash
    docker compose build
    docker compose up -d
    ```

4.  **Done!**
    * The blog is now accessible at `http://localhost:5480` (or `http://your_server_ip:5480`).
    * The admin user you defined in `.env` is automatically created on first launch.

---

### ⚙️ Configuration (`.env` File)

Create a `.env` file in the project root. This file is **required** by Docker Compose.

```env
# --- Site Settings ---
# This will be displayed on the homepage "Hi, I'm [Name]"
BLOG_OWNER_NAME=Chiya

# --- Admin User Configuration (for first launch) ---
ADMIN_USER=admin
ADMIN_PASSWORD=your_secure_password_here
ADMIN_EMAIL=admin@example.com

# --- PostgreSQL Configuration ---
# (Used by the 'db' service)
POSTGRES_USER=mybloguser
POSTGRES_PASSWORD=myblogpassword
POSTGRES_DB=myblogdb

# --- FastAPI Configuration ---
# (Used by the 'backend' service)
# Note: 'db' is the service name from docker-compose.yml
DATABASE_URL=postgresql://mybloguser:myblogpassword@db/myblogdb
```

### 📄 License
This project is licensed under the MIT License. Copyright (c) 2025 Kanzaki Chiya.
