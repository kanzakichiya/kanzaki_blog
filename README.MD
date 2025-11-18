# Kanzaki Chiya's Blog (全栈博客系统)

一个从零开始构建的现代全栈博客系统。使用 FastAPI (后端) + Vue 3 (前端) + PostgreSQL。本项目已通过 Docker, Nginx 和 Postgres 完全容器化，可实现简单、高性能的一键部署。

**[English Version (英文版)](README_EN.MD)**

---

### ✨ 项目功能

* **完整的文章管理**: 针对文章的 CRUD (创建、读取、更新、删除) 操作。
* **安全认证**: 基于 JWT 的用户认证 (注册/登录)，以及受保护的管理员路由和前端路由守卫。
* **现代编辑器**: 集成 **ByteMD** Markdown 编辑器，支持实时预览、语法高亮和安全的图片上传。
* **标签系统**: 功能齐全的标签管理 (创建、删除、分配) 和基于标签的文章筛选 (例如 `/tags/1`)。
* **容器化**: 使用 Docker Compose 完全容器化，可一键部署 (`db` 数据库, `backend` 后端, `frontend` 前端)。

### 🛠️ 技术栈

* **后端**:
    * Python 3.11
    * FastAPI (ASGI 框架)
    * SQLModel (ORM)
    * PostgreSQL (数据库)
    * JWT (认证)
    * Bcrypt (密码哈希)
* **前端**:
    * Vue 3 (组合式 API)
    * Vue Router (路由)
    * Pinia (状态管理)
    * ByteMD (Markdown 编辑器)
* **部署**:
    * Docker & Docker Compose
    * Nginx (作为反向代理和静态文件服务器)

---

### 🚀 快速上手 (生产环境 - Docker)

这是在服务器上部署应用程序最简单且推荐的方式。

1.  **克隆仓库:**
    ```bash
    git clone [https://github.com/your-username/my_blog_project.git](https://github.com/your-username/my_blog_project.git)
    cd my_blog_project
    ```

2.  **创建配置文件:**
    在项目根目录中创建一个名为 `.env` 的文件，复制下面的模板内容，并填写你想要的管理员和数据库密码。

3.  **构建并运行:**
    ```bash
    docker-compose build
    docker-compose up -d
    ```

4.  **完成!**
    * 博客现在可以通过 `http://localhost:5480` (或 `http://你的服务器IP:5480`) 访问。
    * 你在 `.env` 文件中定义的管理员帐户将在首次启动时自动创建。

---

### ⚙️ 配置 (`.env` 文件)

在项目根目录创建一个 `.env` 文件。这是 Docker Compose 运行**所必需的**。

```env
# --- 管理员帐户配置 (首次启动时自动创建) ---
ADMIN_USER=admin
ADMIN_PASSWORD=your_secure_password_here
ADMIN_EMAIL=admin@example.com

# --- PostgreSQL 配置 ---
# (供 'db' 服务使用)
POSTGRES_USER=mybloguser
POSTGRES_PASSWORD=myblogpassword
POSTGRES_DB=myblogdb

# --- FastAPI 配置 ---
# (供 'backend' 服务使用)
# 注意: 'db' 是 docker-compose.yml 中定义的服务名
DATABASE_URL=postgresql://mybloguser:myblogpassword@db/myblogdb
```

### 📄 许可证
本项目基于 MIT 许可证。版权所有 (c) 2025 Kanzaki Chiya。