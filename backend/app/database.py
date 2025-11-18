# backend/app/database.py
from sqlmodel import SQLModel, create_engine, Session
import os # 导入 os

# 1. 从环境变量读取数据库 URL
# 我们将在 docker-compose.yml 中定义这个
DATABASE_URL = os.environ.get("DATABASE_URL")

# 2. 如果 Docker 环境变量不存在 (比如你还在本地开发)，
#    则回退到使用 SQLite
if not DATABASE_URL:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
else:
    # 3. 使用 PostgreSQL
    # (我们不需要 check_same_thread)
    engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session