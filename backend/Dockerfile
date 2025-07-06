# 使用轻量级 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制当前文件夹下所有内容到容器的 /app
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run 默认端口是 $PORT 环境变量
ENV PORT=8080

# 公开端口
EXPOSE 8080

# 启动 Flask 应用
CMD ["python", "app.py"]

