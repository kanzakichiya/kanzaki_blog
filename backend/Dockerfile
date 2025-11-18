# 1. 使用官方 Python 镜像
FROM python:3.11-slim

# 2. 设置工作目录
WORKDIR /app

# 3. (可选) 安装 pip 依赖，以便在本地开发中使用
# RUN pip install --no-cache-dir --upgrade pip
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# 3. (推荐) 安装所有依赖
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir "fastapi[all]" "sqlmodel" "psycopg2-binary" "passlib[bcrypt]" "python-jose[cryptography]" "bcrypt"

# 4. 复制你的应用代码
COPY ./app /app/app
COPY ./static /app/static

# 5. 暴露端口 (和 uvicorn 一致)
EXPOSE 8081

# 6. 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]