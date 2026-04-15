# CI/CD 平台配置指南

本文档提供详细的 CI/CD 平台配置步骤。

---

## 目录

1. [GitHub Actions 配置](#github-actions-配置)
2. [GitLab CI 配置](#gitlab-ci-配置)
3. [Jenkins 配置](#jenkins-配置)
4. [通用配置](#通用配置)

---

## GitHub Actions 配置

### 步骤 1: 初始化 Git 仓库

```bash
cd C:\Users\Administrator\clawd\api_test_suite

# 初始化 Git 仓库
git init

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: API test suite with CI/CD"

# 推送
git branch -M main
git push -u origin main
```

### 步骤 2: 配置 GitHub Secrets

在 GitHub 仓库页面，进入 **Settings → Secrets and variables → Actions**，添加以下 Secrets：

| Secret 名称 | 描述 | 示例值 |
|------------|------|--------|
| `TEST_AUTH` | 测试环境认证信息 | `{"Authorization": "Basic xxx", "Blade-Auth": "Bearer xxx"}` |
| `STAGING_AUTH` | 预发环境认证信息 | `{"Authorization": "Basic xxx", "Blade-Auth": "Bearer xxx"}` |
| `PRODUCTION_AUTH` | 生产环境认证信息 | `{"Authorization": "Basic xxx", "Blade-Auth": "Bearer xxx"}` |
| `SLACK_WEBHOOK` | Slack 通知 Webhook | `https://hooks.slack.com/services/xxx/xxx/xxx` |

### 步骤 3: 启用 GitHub Actions

1. 进入仓库的 **Actions** 标签页
2. 如果看到提示，点击 **I understand my workflows, go ahead and enable them**
3. 工作流将自动运行

### 步骤 4: 手动触发工作流

1. 进入 **Actions** 标签页
2. 选择 **API Regression Test** 工作流
3. 点击 **Run workflow**
4. 选择环境和版本标签
5. 点击 **Run workflow**

### 步骤 5: 查看测试报告

1. 工作流运行完成后，进入运行详情页
2. 在 **Artifacts** 部分下载测试报告：
   - `test-results-test`: 测试环境报告
   - `test-results-staging`: 预发环境报告
   - `allure-results-test`: Allure 报告数据

---

## GitLab CI 配置

### 步骤 1: 推送代码到 GitLab

```bash
cd C:\Users\Administrator\clawd\api_test_suite

# 添加远程仓库
git remote add gitlab https://gitlab.com/YOUR_USERNAME/YOUR_REPO.git

# 推送
git push gitlab main
```

### 步骤 2: 配置 GitLab CI/CD 变量

在 GitLab 项目页面，进入 **Settings → CI/CD → Variables**，添加以下变量：

| 变量名称 | 描述 | 类型 | 保护 |
|---------|------|------|------|
| `TEST_AUTH` | 测试环境认证 | File | 是 |
| `STAGING_AUTH` | 预发环境认证 | File | 是 |
| `SLACK_WEBHOOK` | Slack Webhook | Variable | 是 |

### 步骤 3: 配置 Schedule（定时任务）

1. 进入 **CI/CD → Schedules**
2. 点击 **New schedule**
3. 配置：
   - **Description**: 每日 API 回归测试
   - **Interval Pattern**: Custom: `0 2 * * *`
   - **Target Branch**: main
4. 点击 **Save pipeline schedule**

### 步骤 4: 查看测试报告

1. 进入 **CI/CD → Pipelines**
2. 点击具体的 Pipeline
3. 在 **Jobs** 部分查看测试结果
4. 点击 **Browse** 查看报告文件

---

## Jenkins 配置

### 步骤 1: 安装必要插件

在 Jenkins 中安装以下插件：

1. **Pipeline**: 支持 Jenkinsfile
2. **Git**: Git 支持
3. **Docker**: Docker 支持
4. **Allure**: Allure 报告
5. **HTML Publisher**: HTML 报告发布
6. **JUnit**: JUnit 测试结果

**安装步骤：**

1. 进入 **Manage Jenkins → Plugins**
2. 点击 **Available plugins**
3. 搜索并安装上述插件
4. 重启 Jenkins

### 步骤 2: 创建 Pipeline 项目

1. 点击 **New Item**
2. 输入项目名称，如 `API-Regression-Test`
3. 选择 **Pipeline**
4. 点击 **OK**

### 步骤 3: 配置 Pipeline

在项目配置页面：

**General:**
- 勾选 **This project is parameterized**
- 添加 String Parameter:
  - 名称: `ENVIRONMENT`
  - 默认值: `test`

**Build Triggers:**
- 勾选 **Build periodically**
  - Schedule: `H 2 * * *`（每日凌晨 2 点）

**Pipeline:**
- Definition: Pipeline script from SCM
- SCM: Git
- Repository URL: `https://github.com/YOUR_USERNAME/YOUR_REPO.git`
- Branch Specifier: `*/main`
- Script Path: `Jenkinsfile`

### 步骤 4: 配置 Credentials

1. 进入 **Manage Jenkins → Credentials**
2. 添加以下 Credentials：

| ID | 类型 | 描述 |
|----|------|------|
| `slack-webhook-url` | Secret text | Slack Webhook URL |
| `test-auth` | Secret text | 测试环境认证 |
| `staging-auth` | Secret text | 预发环境认证 |

### 步骤 5: 手动触发构建

1. 进入项目页面
2. 点击 **Build with Parameters**
3. 选择环境参数
4. 点击 **Build**

### 步骤 6: 查看测试报告

1. 进入构建详情页
2. 点击 **Test Result** 查看 JUnit 报告
3. 点击 **Allure Report** 查看 Allure 报告
4. 点击 **HTML Report** 查看 HTML 报告

---

## 通用配置

### Docker 支持

创建 `Dockerfile` 用于测试环境：

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["pytest"]
```

### Docker Compose

创建 `docker-compose.yml` 用于本地测试：

```yaml
version: '3.8'

services:
  api-test:
    build: .
    volumes:
      - ./reports:/app/reports
    environment:
      - BASE_URL=http://106.227.91.110:31000/api
    command: pytest -v --html=reports/report.html
```

### 环境变量配置

创建 `.env` 文件（不要提交到 Git）：

```env
# .env
BASE_URL=http://106.227.91.110:31000/api
AUTHORIZATION=Basic c2FiZXIzOnNhYmVyM19zZWNyZXQ=
BLADE_AUTH=bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Git 忽略配置

创建 `.gitignore`：

```gitignore
# .gitignore
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.coverage
htmlcov/
*.xml
*.html
allure-results/
allure-report/
.env
*.log
reports/
.venv/
venv/
```

---

## 通知配置

### Slack Webhook 配置

1. 在 Slack 工作区创建 Incoming Webhook：
   - 进入 **Apps → Incoming Webhooks**
   - 点击 **Add to Slack**
   - 选择通知频道
   - 复制 Webhook URL

2. 测试 Webhook：

```bash
curl -X POST "YOUR_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{"text": "测试通知"}'
```

### 钉钉 Webhook 配置

```bash
curl -X POST "YOUR_DINGTALK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "text",
    "text": {"content": "API 回归测试完成"}
  }'
```

### 企业微信 Webhook 配置

```bash
curl -X POST "YOUR_WECHAT_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "text",
    "text": {"content": "API 回归测试完成"}
  }'
```

---

## 验证配置

### 本地验证

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest -v --tb=short

# 检查代码风格
pip install flake8 black isort
flake8 . --max-line-length=120
black --check .
isort --check-only .

# 生成报告
pytest --html=report.html --self-contained-html
```

### CI/CD 验证

推送代码后，检查：

1. ✅ Pipeline 是否成功触发
2. ✅ 测试是否全部通过
3. ✅ 报告是否正确生成
4. ✅ 通知是否正常发送

---

## 故障排查

### 常见问题

**1. Pipeline 触发失败**

```bash
# 检查 Webhook 配置
# GitHub: Settings → Webhooks
# GitLab: Settings → Webhooks
```

**2. 测试环境连接失败**

```bash
# 检查网络连通性
curl http://106.227.91.110:31000/api

# 检查认证信息
# 确保 Secrets 配置正确
```

**3. 报告生成失败**

```bash
# 检查 Allure 安装
allure --version

# 手动生成报告
allure generate allure-results/ -o allure-report/
```

**4. 通知发送失败**

```bash
# 测试 Webhook
curl -X POST "YOUR_WEBHOOK" -d '{"text": "test"}'
```

---

## 下一步

1. 根据实际使用的 CI/CD 平台，选择对应的配置步骤
2. 配置必要的 Secrets 和环境变量
3. 推送代码并验证 Pipeline 运行
4. 根据测试结果调整测试用例和配置

如有问题，请参考各平台的官方文档或联系技术支持。
