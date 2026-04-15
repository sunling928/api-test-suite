# GitHub Personal Access Token 创建指南

## 步骤 1：登录 GitHub

打开 https://github.com 并登录你的账号

---

## 步骤 2：进入 Token 创建页面

两种方式：

**方式 A：直接访问**
https://github.com/settings/tokens/new?scopes=repo

**方式 B：手动导航**
1. 点击右上角头像 → **Settings**
2. 左侧底部找到 **Developer settings**
3. 点击 **Personal access tokens** → **Tokens (classic)**
4. 点击 **Generate new token** → **Generate new token (classic)**

---

## 步骤 3：配置 Token

### 基本信息

| 字段 | 值 |
|-----|-----|
| **Note** | `API Test Suite`（描述） |
| **Expiration** | `No expiration`（永不过期）或选择 30/60/90 天 |

### 权限选择（必须勾选）

✅ 勾选以下权限：

- **[✓] repo** (Full control of private repositories)
  - [✓] repo:status
  - [✓] repo_deployment
  - [✓] public_repo
  - [✓] repo:invite

---

## 步骤 4：生成 Token

1. 点击 **Generate token**
2. **重要**：Token 只显示一次！
3. 复制并妥善保存 Token

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **警告**：Token 只会显示一次，刷新页面后将无法查看！

---

## 步骤 5：使用 Token 推送代码

### 方法 A：命令行

```bash
cd C:\Users\Administrator\clawd\api_test_suite
git remote add origin https://github.com/sunling928/api-test-suite.git
git push -u origin master
```

当提示输入密码时：
- **Username**: `sunling928`
- **Password**: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`（粘贴你的 Token）

### 方法 B：使用推送脚本

```batch
push_to_github.bat
```

---

## 步骤 6：验证推送成功

1. 打开 https://github.com/sunling928/api-test-suite
2. 确认代码已上传

---

## 常见问题

### Q: Token 提示无效
A: 确保完整复制 Token，包括 `ghp_` 前缀

### Q: 推送时提示权限不足
A: 确认 Token 已勾选 `repo` 权限

### Q: 如何撤销 Token
A: Settings → Developer settings → Tokens → Revoke

### Q: Token 泄露了怎么办
A: 立即撤销：Settings → Developer settings → Tokens → Revoke，然后重新生成

---

## 安全建议

1. ✅ 不要将 Token 提交到代码仓库
2. ✅ 使用 GitHub Actions Secrets 存储 Token
3. ✅ 定期更换 Token
4. ✅ 使用 SSH 密钥代替 Token（更安全）

---

## 后续配置 CI/CD

Token 创建完成后，还需要配置：

1. **添加 Secrets**：
   - Settings → Secrets and variables → Actions
   - 添加 `TEST_AUTH`（认证信息）

2. **触发 CI/CD**：
   - 推送代码后，Actions 会自动运行

---

如有疑问，请联系开发者！
