# 使用 Python 3.10 作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 安装必要的系统库
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender1
    
# 复制 requirements.txt
COPY requirements.txt /app/

# 安装依赖
RUN pip install -r requirements.txt

# 复制应用代码
COPY . /app/

# 暴露端口
EXPOSE 9000

# 启动 Flask 应用
CMD ["python", "app.py"]