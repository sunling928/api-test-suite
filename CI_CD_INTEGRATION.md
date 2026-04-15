# API 测试套件 CI/CD 集成指南

## 概述

本测试套件支持多种 CI/CD 平台的集成：
- GitHub Actions
- GitLab CI/CD
- Jenkins
- 手动触发

## 快速开始

### 1. 本地运行测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行所有测试
pytest test_order_submit.py -v

# 运行特定测试类
pytest test_order_submit.py::TestOrderSubmit -v

# 生成 HTML 报告
pytest test_order_submit.py --html=report.html --self-contained-html
```

### 2. Windows 快速运行

```batch
# 运行测试（双击或在命令行执行）
run_tests.bat
```

## GitHub Actions 集成

### 配置步骤

1. 确保仓库已启用 GitHub Actions
2. 配置 Secrets：
   - `TEST_AUTH`: 测试环境认证信息
   - `STAGING_AUTH`: 预发环境认证信息
   - `SLACK_WEBHOOK`: Slack 通知 Webhook（可选）

3. 触发方式：
   - **定时任务**: 每天凌晨 2:00 自动运行
   - **代码推送**: 当 `api_test_suite/` 或 `openapi.yaml` 变更时触发
   - **手动触发**: 通过 GitHub Actions 页面选择环境和版本

### 工作流文件

位置: `.github/workflows/regression.yml`

```yaml
# 主要触发条件
on:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨
  push:
    paths:
      - 'api_test_suite/**'
      - 'openapi.yaml'
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [test, staging, production]
```

## GitLab CI 集成

### 配置步骤

1. 配置 CI/CD 变量：
   - `TEST_AUTH`: 认证信息
   - `SLACK_WEBHOOK`: Slack Webhook

2. 确保 `.gitlab-ci.yml` 在项目根目录

3. 触发方式：
   - MR 合并时
   - 推送到 main 分支
   - 定时任务（ schedules）

### 流水线阶段

```
lint → regression-test → api-change-detect → allure-report → notify
```

## Jenkins 集成

### 配置步骤

1. 安装必要插件：
   - Pipeline
   - Allure Plugin
   - HTML Publisher Plugin

2. 配置凭据：
   - `slack-webhook-url`: Slack Webhook

3. 创建 Pipeline 任务：
   - 选择 "Pipeline script from SCM"
   - 配置仓库 URL
   - 指定 `Jenkinsfile` 路径

### 触发器

```groovy
triggers {
    cron('0 2 * * *')  // 每天凌晨
    gitlab(triggerOnPush: true, triggerOnMergeRequest: true)
}
```

## API 变更检测

### 工作原理

1. 每次 CI/CD 运行时，对比 `openapi.yaml` 与上一版本
2. 检测以下变更：
   - 新增/删除/修改的端点
   - 新增/删除/修改的参数
   - 新增/删除/修改的 Schema

3. 生成变更报告 (`change_report.json`)

4. 根据变更自动生成受影响的测试用例

### 手动检测

```bash
python .github/scripts/detect_api_change.py \
    --old-spec=openapi_old.yaml \
    --new-spec=openapi.yaml \
    --output=change_report.json
```

## 环境配置

### 测试环境

| 变量 | 值 |
|-----|-----|
| BASE_URL | http://106.227.91.110:31000/api |
| ENVIRONMENT | test |

### 预发环境

| 变量 | 值 |
|-----|-----|
| BASE_URL | http://staging-api.example.com/api |
| ENVIRONMENT | staging |

### 生产环境（仅手动触发）

| 变量 | 值 |
|-----|-----|
| BASE_URL | http://prod-api.example.com/api |
| ENVIRONMENT | production |

## 测试报告

### 生成 HTML 报告

```bash
pytest test_order_submit.py --html=report.html --self-contained-html
```

### 生成 Allure 报告

```bash
# 生成 Allure 结果
pytest test_order_submit.py --alluredir=allure-results

# 生成报告（需要 Allure CLI）
allure serve allure-results
```

### 查看 JUnit XML 报告

JUnit XML 格式的报告会自动生成，文件名格式：
- `results_{environment}_{test_file}.xml`

## 通知配置

### Slack 通知

配置 `SLACK_WEBHOOK` 环境变量，测试失败时自动发送通知：

```json
{
  "text": "API 回归测试失败!",
  "attachments": [{
    "color": "danger",
    "fields": [
      {"title": "环境", "value": "test", "short": true},
      {"title": "分支", "value": "main", "short": true}
    ]
  }]
}
```

## 故障排查

### 常见问题

1. **认证失败**
   - 检查 `conftest.py` 中的 `PREDEFINED_AUTH` 是否有效
   - 确保 Secrets 配置正确

2. **连接超时**
   - 检查 BASE_URL 是否正确
   - 确认网络连通性

3. **测试失败**
   - 查看 HTML 报告获取详细错误信息
   - 使用 `-v -s` 参数查看详细输出

### 调试模式

```bash
# 详细输出
pytest test_order_submit.py -v -s

# 只运行失败的测试
pytest test_order_submit.py --lf

# 停在第一个失败
pytest test_order_submit.py -x
```

## 维护

### 添加新测试

1. 在 `test_order_submit.py` 中添加测试方法
2. 确保使用 `auth_headers` fixture 进行认证
3. 使用 `OrderTestData` 类生成测试数据

### 更新 API 规范

1. 从 Apifox 导出 OpenAPI 规范
2. 保存为 `openapi.yaml`
3. 提交到仓库触发 CI/CD

## 许可证

MIT License
