# --- 阶段 1: 构建 (Build Stage) ---
# 使用 Node.js 镜像来构建 Vue 应用
FROM node:20-alpine AS build

WORKDIR /app

# 复制 package.json 并安装依赖
COPY package.json .
COPY package-lock.json .
RUN npm install

# 复制所有源代码并构建
COPY . .
RUN npm run build

# --- 阶段 2: 运行 (Serve Stage) ---
# 使用轻量级的 Nginx 镜像来提供服务
FROM nginx:1.25-alpine

# 从 "build" 阶段复制打包好的静态文件到 Nginx 的 HTML 目录
COPY --from=build /app/dist /usr/share/nginx/html

# 复制我们自定义的 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露 Nginx 的 80 端口
EXPOSE 80
