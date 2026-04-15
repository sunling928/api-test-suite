@echo off
chcp 65001 >nul
echo ========================================
echo   API 测试套件 - 自动化测试运行器
echo ========================================
echo.

REM 设置 Python 路径
set PYTHON_EXE=C:\Program Files\Python313\python.exe
set PYTEST_CMD=%PYTHON_EXE% -m pytest

REM 检查 Python 是否存在
if not exist "%PYTHON_EXE%" (
    echo [错误] Python 未找到: %PYTHON_EXE%
    echo 请修改脚本中的 PYTHON_EXE 变量
    pause
    exit /b 1
)

REM 解析参数
set TEST_ENV=%1
if "%TEST_ENV%"=="" set TEST_ENV=all

echo [信息] 测试环境: %TEST_ENV%
echo [信息] Python: %PYTHON_EXE%
echo.

REM 切换到脚本目录
cd /d "%~dp0"

REM 检查依赖
echo [步骤 1/3] 检查依赖...
%PYTHON_EXE% -c "import pytest, requests" 2>nul
if errorlevel 1 (
    echo [警告] 依赖未安装，正在安装...
    %PYTHON_EXE% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)
echo [完成] 依赖检查通过
echo.

REM 运行测试
echo [步骤 2/3] 运行测试...
echo ========================================

if "%TEST_ENV%"=="all" (
    echo 运行所有测试...
    %PYTEST_CMD% test_order_submit.py test_order.py -v --tb=short --html=report.html --self-contained-html --alluredir=allure-results
) else if "%TEST_ENV%"=="order" (
    echo 运行订单提交测试...
    %PYTEST_CMD% test_order_submit.py -v --tb=short --html=report_order.html --self-contained-html
) else if "%TEST_ENV%"=="quick" (
    echo 快速测试（仅正向测试）...
    %PYTEST_CMD% test_order_submit.py::TestOrderSubmit::test_submit_order_success -v --tb=short
) else (
    echo 运行指定测试: %TEST_ENV%
    %PYTEST_CMD% %TEST_ENV% -v --tb=short --html=report.html --self-contained-html
)

set TEST_EXIT_CODE=%errorlevel%
echo.

REM 生成摘要
echo [步骤 3/3] 生成测试摘要...
echo ========================================

if exist report.html (
    echo [完成] HTML 报告已生成: report.html
    start report.html
)

if exist allure-results (
    echo [提示] Allure 结果已生成: allure-results/
    echo        运行 'allure serve allure-results' 查看报告
)

echo.
echo ========================================
if %TEST_EXIT_CODE%==0 (
    echo [成功] 所有测试通过！
) else (
    echo [失败] 部分测试失败，请查看报告
)
echo ========================================
echo.

pause
exit /b %TEST_EXIT_CODE%
