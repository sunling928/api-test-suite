#!/usr/bin/env python3
"""
快速配置脚本
用于初始化测试环境和 CI/CD 配置
"""
import os
import sys
import json
import argparse
from pathlib import Path


def create_env_file():
    """创建 .env 文件"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("[OK] .env 文件已存在")
        return
    
    if env_example.exists():
        # 复制示例文件
        content = env_example.read_text(encoding='utf-8')
        env_file.write_text(content, encoding='utf-8')
        print("[OK] 已创建 .env 文件")
        print("[INFO] 请编辑 .env 文件，填入实际配置值")
    else:
        # 创建默认配置
        default_env = """# API 基础 URL
BASE_URL=http://106.227.91.110:31000/api

# 运行环境
ENVIRONMENT=test

# 认证信息
AUTHORIZATION=Basic c2FiZXIzOnNhYmVyM19zZWNyZXQ=
BLADE_AUTH=bearer YOUR_TOKEN_HERE

# 测试配置
TEST_TIMEOUT=300
"""
        env_file.write_text(default_env, encoding='utf-8')
        print("[OK] 已创建 .env 文件")


def create_gitignore():
    """创建 .gitignore 文件"""
    gitignore = Path(".gitignore")
    
    if gitignore.exists():
        print("[OK] .gitignore 已存在")
        return
    
    content = """# Python
__pycache__/
*.py[cod]
*.pyo
.pytest_cache/
.coverage
htmlcov/

# Reports
reports/
allure-results/
allure-report/
*.xml
*.html

# Environment
.env
*.log

# IDE
.vscode/
.idea/
"""
    gitignore.write_text(content, encoding='utf-8')
    print("[OK] 已创建 .gitignore 文件")


def init_git_repo():
    """初始化 Git 仓库"""
    import subprocess
    
    try:
        # 检查是否已是 Git 仓库
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("[OK] Git 仓库已存在")
            return
        
        # 初始化仓库
        subprocess.run(["git", "init"], check=True)
        print("[OK] 已初始化 Git 仓库")
        
    except FileNotFoundError:
        print("[ERROR] Git 未安装，请先安装 Git")
    except Exception as e:
        print(f"[ERROR] Git 初始化失败: {e}")


def install_dependencies():
    """安装依赖"""
    import subprocess
    
    try:
        print("正在安装依赖...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("[OK] 依赖安装完成")
    except Exception as e:
        print(f"[ERROR] 依赖安装失败: {e}")


def run_tests():
    """运行测试"""
    import subprocess
    
    try:
        print("正在运行测试...")
        subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "--tb=short"],
            check=True
        )
        print("[OK] 测试运行完成")
    except Exception as e:
        print(f"[ERROR] 测试运行失败: {e}")


def generate_report():
    """生成测试报告"""
    import subprocess
    
    try:
        print("正在生成报告...")
        subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "--html=report.html",
                "--self-contained-html",
                "--alluredir=allure-results"
            ],
            check=True
        )
        print("[OK] 报告生成完成: report.html")
    except Exception as e:
        print(f"[ERROR] 报告生成失败: {e}")


def setup_github_actions():
    """设置 GitHub Actions"""
    workflows_dir = Path(".github/workflows")
    
    if workflows_dir.exists():
        print("[OK] GitHub Actions 已配置")
        print("   工作流文件: .github/workflows/regression.yml")
    else:
        print("[WARN] GitHub Actions 配置未找到")
        print("   请确保 .github/workflows/ 目录存在")


def setup_gitlab_ci():
    """设置 GitLab CI"""
    gitlab_ci = Path(".gitlab-ci.yml")
    
    if gitlab_ci.exists():
        print("[OK] GitLab CI 已配置")
        print("   配置文件: .gitlab-ci.yml")
    else:
        print("[WARN] GitLab CI 配置未找到")


def setup_jenkins():
    """设置 Jenkins"""
    jenkinsfile = Path("Jenkinsfile")
    
    if jenkinsfile.exists():
        print("[OK] Jenkins 已配置")
        print("   配置文件: Jenkinsfile")
    else:
        print("[WARN] Jenkins 配置未找到")


def show_status():
    """显示配置状态"""
    print("\n" + "=" * 50)
    print("API 测试套件配置状态")
    print("=" * 50)
    
    checks = [
        (".env", "环境配置"),
        (".gitignore", "Git 忽略配置"),
        ("requirements.txt", "依赖配置"),
        ("conftest.py", "Pytest 配置"),
        ("test_order.py", "测试用例"),
        (".github/workflows/regression.yml", "GitHub Actions"),
        (".gitlab-ci.yml", "GitLab CI"),
        ("Jenkinsfile", "Jenkins"),
        ("Dockerfile", "Docker"),
        ("docker-compose.yml", "Docker Compose"),
    ]
    
    for file_path, description in checks:
        exists = Path(file_path).exists()
        status = "[OK]" if exists else "[MISSING]"
        print(f"{status} {description}: {file_path}")
    
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="API 测试套件配置工具")
    
    parser.add_argument(
        "action",
        choices=[
            "init", "install", "test", "report",
            "status", "git", "github", "gitlab", "jenkins",
            "all"
        ],
        help="执行的操作"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 50)
    print("API 测试套件配置工具")
    print("=" * 50 + "\n")
    
    if args.action == "init":
        create_env_file()
        create_gitignore()
        init_git_repo()
        
    elif args.action == "install":
        install_dependencies()
        
    elif args.action == "test":
        run_tests()
        
    elif args.action == "report":
        generate_report()
        
    elif args.action == "status":
        show_status()
        
    elif args.action == "git":
        init_git_repo()
        
    elif args.action == "github":
        setup_github_actions()
        
    elif args.action == "gitlab":
        setup_gitlab_ci()
        
    elif args.action == "jenkins":
        setup_jenkins()
        
    elif args.action == "all":
        create_env_file()
        create_gitignore()
        init_git_repo()
        install_dependencies()
        show_status()
        print("\n[OK] 配置完成！")
        print("\n下一步:")
        print("1. 编辑 .env 文件，填入实际配置")
        print("2. 运行测试: python setup.py test")
        print("3. 生成报告: python setup.py report")


if __name__ == "__main__":
    main()
