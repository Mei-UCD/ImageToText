# 使用轻量级 Python 镜像
FROM python:3.10-slim

# 安装 EasyOCR 和 OpenCV 所需的系统库
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

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

