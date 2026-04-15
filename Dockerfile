# API Test Suite Dockerfile
# 用于 CI/CD 环境中的测试执行

FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Allure 命令行工具
RUN curl -L https://allure-downloads.jetbrains.com/jenkins/latest.tgz | tar -xz -C /tmp && \
    mv /tmp/allure-*/bin/allure /usr/local/bin/ && \
    rm -rf /tmp/allure-*

# 复制测试代码
COPY . .

# 创建报告目录
RUN mkdir -p reports allure-results

# 默认命令
CMD ["pytest", "-v", "--tb=short"]
