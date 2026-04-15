@echo off
chcp 65001 >nul
echo ========================================
echo   GitHub 仓库推送脚本
echo ========================================
echo.

REM 切换到项目目录
cd /d "%~dp0"

REM 检查 Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Git 未安装
    echo 请从 https://git-scm.com/downloads 下载安装 Git
    pause
    exit /b 1
)

echo [信息] 当前目录: %CD%
echo.

REM 显示当前状态
echo [步骤 1/4] 检查 Git 状态...
git status -sb
echo.

REM 检查远程仓库
echo [步骤 2/4] 检查远程仓库...
git remote -v
if errorlevel 1 (
    echo [设置] 添加远程仓库...
    git remote add origin https://github.com/sunling928/api-test-suite.git
)
echo.

REM 显示提交历史
echo [步骤 3/4] 显示提交历史...
git log --oneline -5
echo.

REM 推送代码
echo [步骤 4/4] 推送代码到 GitHub...
echo ========================================
echo.
echo 注意：如果需要认证，请输入 GitHub 用户名和密码
echo 或使用 Personal Access Token 作为密码
echo.

git push -u origin master

if errorlevel 1 (
    echo.
    echo ========================================
    echo [失败] 推送失败！
    echo.
    echo 可能的原因：
    echo 1. 网络连接问题 - 检查是否能访问 github.com
    echo 2. 认证失败 - 需要输入正确的用户名和密码/Token
    echo 3. 仓库不存在 - 请先在 GitHub 创建仓库
    echo.
    echo 解决方案：
    echo.
    echo 方案 A：使用 SSH（推荐）
    echo   1. 生成 SSH 密钥：ssh-keygen -t ed25519 -C "your@email.com"
    echo   2. 添加到 GitHub：https://github.com/settings/keys
    echo   3. 切换到 SSH：git remote set-url origin git@github.com:sunling928/api-test-suite.git
    echo   4. 重新运行此脚本
    echo.
    echo 方案 B：使用 Personal Access Token
    echo   1. 创建 Token：https://github.com/settings/tokens
    echo   2. 勾选 repo 权限
    echo   3. 推送时使用 Token 作为密码
    echo.
    echo 方案 C：配置代理（如果有）
    echo   git config --global http.proxy http://代理地址:端口
    echo   git config --global https.proxy http://代理地址:端口
    echo ========================================
) else (
    echo.
    echo ========================================
    echo [成功] 代码已推送到 GitHub！
    echo.
    echo 仓库地址：https://github.com/sunling928/api-test-suite
    echo.
    echo 下一步：
    echo 1. 配置 GitHub Actions Secrets
    echo 2. 查看 Actions 页面确认 CI/CD 运行
    echo ========================================
)

echo.
pause
