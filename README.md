# 订单接口测试套件

基于 Apifox 导出的 OpenAPI 规范自动生成的 Pytest + Requests 接口测试套件。

## 目录结构

```
api_test_suite/
├── .github/
│   ├── workflows/
│   │   └── regression.yml      # GitHub Actions 配置
│   └── scripts/
│       ├── detect_api_change.py    # API 变更检测
│       ├── generate_affected_tests.py  # 生成受影响测试
│       └── summary.py              # 测试报告生成
├── .gitlab-ci.yml               # GitLab CI 配置
├── Jenkinsfile                  # Jenkins 流水线
├── conftest.py                  # Pytest 配置（认证、客户端、断言）
├── test_data.py                 # 参数化测试数据
├── test_order.py                # 测试用例
├── pytest.ini                   # Pytest 配置
├── requirements.txt             # Python 依赖
└── README.md                    # 本文件
```

---

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试
pytest test_order.py::TestOrderSubmit -v

# 生成 HTML 报告
pytest --html=report.html --self-contained-html

# 生成 Allure 报告
pytest --alluredir=./allure-results
allure serve ./allure-results
```

---

## 核心特性

### 1. 自动 Token 认证

```python
from conftest import token_manager, auth_headers

# 手动设置 Token
token_manager.set_token("your_token_here", expires_in=7200)

# 自动刷新（当 Token 过期时）
token = token_manager.get_token(force_refresh=True)
```

### 2. 参数化测试

```python
from test_data import (
    get_positive_cases,    # 正向测试用例
    get_negative_cases,    # 异常测试用例
    get_boundary_cases,    # 边界值测试用例
    generate_order_data    # 数据生成器
)

# 使用参数化
@pytest.mark.parametrize("case", get_positive_cases(), ids=lambda c: c["name"])
def test_submit_order_success(self, case):
    ...
```

### 3. 响应断言封装

```python
from conftest import assert_response

# 链式调用
assert_response(response) \
    .status_code(200) \
    .success() \
    .has_field("resultCode") \
    .field_equals("resultCode", 0) \
    .print_response()
```

---

## CI/CD 集成

### GitHub Actions

```yaml
# .github/workflows/regression.yml
name: API Regression Test

on:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨2点
  push:
    paths:
      - 'api_test_suite/**'
  workflow_dispatch:
```

**配置步骤：**

1. 创建 `.github/workflows/regression.yml`
2. 在仓库设置中添加 Secrets:
   - `TEST_AUTH`: 测试环境认证信息
   - `STAGING_AUTH`: 预发环境认证信息
   - `SLACK_WEBHOOK`: Slack 通知 Webhook

### GitLab CI

```bash
# .gitlab-ci.yml 已配置，包含以下 stages:
# - lint: 代码检查
# - test: 回归测试
# - report: 生成报告
# - notify: 通知
```

**配置步骤：**

1. 复制 `.gitlab-ci.yml` 到项目根目录
2. 在 GitLab CI/CD 设置中添加变量:
   - `SLACK_WEBHOOK`: Slack 通知 Webhook

### Jenkins

```groovy
// Jenkinsfile 已配置
// 流水线包含：Lint -> API变更检测 -> 回归测试 -> 报告 -> 通知
```

**配置步骤：**

1. 在 Jenkins 中创建 Pipeline 项目
2. 配置 Git 仓库和凭证
3. 添加 Slack Webhook 凭据

---

## API 变更检测

### 自动检测流程

```bash
# 1. 检测 API 变更
python .github/scripts/detect_api_change.py \
    --old-spec=openapi_old.yaml \
    --new-spec=openapi.yaml \
    --output=change_report.json

# 2. 生成受影响测试用例
python .github/scripts/generate_affected_tests.py
```

### 变更报告内容

```json
{
  "changes": {
    "added_endpoints": [],
    "removed_endpoints": [],
    "modified_endpoints": [],
    "added_schemas": [],
    "removed_schemas": [],
    "modified_schemas": []
  },
  "test_plan": {
    "affected_tests": [],
    "new_tests_needed": [],
    "priority": "high|medium|low"
  }
}
```

---

## 测试用例清单

### TestOrderSubmit - 订单提交测试

| 测试用例 | 类型 | 描述 |
|---------|------|------|
| test_submit_order_success | 参数化 | 正向场景测试 |
| test_submit_order_validation | 参数化 | 参数校验测试 |
| test_submit_order_boundary | 参数化 | 边界值测试 |
| test_submit_order_batch | 参数化 | 批量数据测试 |

### TestAuth - 认证测试

| 测试用例 | 描述 |
|---------|------|
| test_submit_order_without_auth | 无认证测试 |
| test_submit_order_invalid_token | 无效Token测试 |
| test_token_refresh | Token刷新功能 |

### TestResponseFormat - 响应格式测试

| 测试用例 | 描述 |
|---------|------|
| test_response_schema | 响应结构验证 |
| test_response_code_meaning | 响应码含义 |

### TestPerformance - 性能测试

| 测试用例 | 描述 |
|---------|------|
| test_response_time | 响应时间测试 |

---

## 环境配置

### 测试环境

- **Base URL**: `http://106.227.91.110:31000/api`
- **认证**: Bearer Token (已在 conftest.py 配置)

### 切换环境

```bash
# 通过环境变量切换
export BASE_URL=http://your-api-server/api
pytest
```

---

## 注意事项

1. **Token 配置**: 在 `conftest.py` 中更新 `PREDEFINED_AUTH`
2. **测试数据**: 根据实际业务需求修改 `test_data.py`
3. **CI/CD 密钥**: 确保在 CI/CD 平台中配置必要的密钥
4. **环境隔离**: 不同环境使用不同的认证信息

---

## 许可证

MIT License
