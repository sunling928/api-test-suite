# GitHub 仓库创建指南

## 步骤 1：创建 GitHub 仓库

1. 打开 https://github.com/new
2. 填写以下信息：
   - **Repository name**: `api-test-suite`
   - **Description**: `API 自动化测试套件 - Pytest + Requests`
   - **可见性**: Public（公开）或 Private（私有）
   - **不要勾选**以下选项：
     - Add a README file
     - Add .gitignore  
     - Choose a license

3. 点击 **Create repository**

## 步骤 2：推送代码

创建成功后，GitHub 会显示以下命令：

```bash
# 设置远程仓库地址
git remote add origin https://github.com/你的用户名/api-test-suite.git

# 推送代码
git push -u origin master
```

### 如果你没有 GitHub 账号

1. 注册 GitHub 账号：https://github.com/signup
2. 创建仓库（步骤 1）
3. 推送代码（步骤 2）

## 步骤 3：配置 CI/CD

### GitHub Actions

仓库创建后，GitHub Actions 会自动启用。你需要配置 Secrets：

1. 在仓库页面点击 **Settings**
2. 选择 **Secrets and variables** > **Actions**
3. 添加以下 Secrets：

| Secret 名称 | 值 |
|------------|-----|
| `TEST_AUTH` | `{"Authorization": "Basic c2FiZXI6c2FiZXJfc2VjcmV0", "Blade-Auth": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}` |
| `SLACK_WEBHOOK` | `https://hooks.slack.com/services/...`（可选） |

## 步骤 4：触发 CI/CD

### 自动触发
- 每天凌晨 2:00 自动运行
- 代码变更时自动运行

### 手动触发
1. 在仓库页面点击 **Actions**
2. 选择 **API Regression Test**
3. 点击 **Run workflow**
4. 选择环境（test/staging/production）

## 测试报告查看

### GitHub Actions 报告
1. 运行完成后，点击 **Actions**
2. 选择最新的 workflow
3. 下载 `test-results-test` artifact
4. 查看 HTML 报告

### 本地查看
```bash
# 运行测试
run_tests.bat

# 查看报告
start report.html
```

## 故障排查

### 认证失败
检查 `conftest.py` 中的 `PREDEFINED_AUTH` 是否有效

### 连接失败
检查 `BASE_URL` 是否正确：`http://106.227.91.110:31000/api`

### CI/CD 失败
查看 GitHub Actions 日志，检查 Secrets 配置

## 联系方式

如需帮助，请联系：
- GitHub Issues: 在仓库创建 Issue
- Email: developer@example.com

---

**重要提示**：请确保认证信息保密，不要公开分享！
