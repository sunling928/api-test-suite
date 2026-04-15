#!/usr/bin/env python3
"""
生成测试摘要报告
"""
import xml.etree.ElementTree as ET
import sys
import json
from typing import Dict, Any


def parse_junit_xml(file_path: str) -> Dict[str, Any]:
    """解析 JUnit XML 报告"""
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    summary = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
        "testsuites": []
    }
    
    for testsuite in root.findall('.//testsuite'):
        ts_name = testsuite.get('name', 'unknown')
        ts_tests = int(testsuite.get('tests', 0))
        ts_failures = int(testsuite.get('failures', 0))
        ts_errors = int(testsuite.get('errors', 0))
        ts_skipped = int(testsuite.get('skipped', 0))
        
        test_cases = []
        for testcase in testsuite.findall('.//testcase'):
            tc_name = testcase.get('name', 'unknown')
            tc_classname = testcase.get('classname', '')
            tc_time = float(testcase.get('time', 0))
            
            # 检查失败或错误
            failure = testcase.find('failure')
            error = testcase.find('error')
            
            status = "passed"
            message = ""
            
            if failure is not None:
                status = "failed"
                message = failure.get('message', '')
            elif error is not None:
                status = "error"
                message = error.get('message', '')
            elif testcase.find('skipped') is not None:
                status = "skipped"
            
            test_cases.append({
                "name": tc_name,
                "classname": tc_classname,
                "time": tc_time,
                "status": status,
                "message": message
            })
        
        summary["testsuites"].append({
            "name": ts_name,
            "tests": ts_tests,
            "failures": ts_failures,
            "errors": ts_errors,
            "skipped": ts_skipped,
            "test_cases": test_cases
        })
        
        summary["total"] += ts_tests
        summary["passed"] += ts_tests - ts_failures - ts_errors - ts_skipped
        summary["failed"] += ts_failures
        summary["errors"] += ts_errors
        summary["skipped"] += ts_skipped
    
    return summary


def generate_markdown(summary: Dict[str, Any]) -> str:
    """生成 Markdown 格式报告"""
    
    md = f"""# API 回归测试报告

## 测试摘要

| 指标 | 数量 |
|------|------|
| 总测试数 | {summary['total']} |
| 通过 | ✅ {summary['passed']} |
| 失败 | ❌ {summary['failed']} |
| 错误 | ⚠️ {summary['errors']} |
| 跳过 | ⏭️ {summary['skipped']} |

## 通过率: {summary['passed'] / summary['total'] * 100:.1f}%

"""
    
    # 添加失败的测试详情
    if summary['failed'] > 0 or summary['errors'] > 0:
        md += "\n## 失败详情\n\n"
        
        for ts in summary['testsuites']:
            failed_tests = [tc for tc in ts['test_cases'] if tc['status'] in ['failed', 'error']]
            
            if failed_tests:
                md += f"### {ts['name']}\n\n"
                
                for tc in failed_tests:
                    md += f"- **{tc['name']}** ({tc['classname']})\n"
                    if tc['message']:
                        md += f"  - 错误信息: {tc['message'][:200]}\n"
                    md += "\n"
    
    return md


def generate_slack_message(summary: Dict[str, Any]) -> dict:
    """生成 Slack 消息"""
    
    pass_rate = summary['passed'] / summary['total'] * 100 if summary['total'] > 0 else 0
    
    color = "good" if summary['failed'] == 0 and summary['errors'] == 0 else "danger"
    
    message = {
        "attachments": [{
            "color": color,
            "title": "API 回归测试报告",
            "fields": [
                {"title": "总测试", "value": str(summary['total']), "short": True},
                {"title": "通过", "value": f"✅ {summary['passed']}", "short": True},
                {"title": "失败", "value": f"❌ {summary['failed']}", "short": True},
                {"title": "通过率", "value": f"{pass_rate:.1f}%", "short": True}
            ]
        }]
    }
    
    return message


def main():
    if len(sys.argv) < 2:
        print("用法: python summary.py <junit-xml-file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # 解析报告
    summary = parse_junit_xml(file_path)
    
    # 生成 Markdown 报告
    md_report = generate_markdown(summary)
    
    # 保存报告
    report_file = "test_summary.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"测试摘要报告已生成: {report_file}")
    print(f"\n{md_report}")
    
    # 如果有失败的测试，生成 Slack 消息
    if summary['failed'] > 0 or summary['errors'] > 0:
        slack_msg = generate_slack_message(summary)
        with open("slack_message.json", 'w', encoding='utf-8') as f:
            json.dump(slack_msg, f, indent=2)
        print(f"\nSlack 消息已生成: slack_message.json")


if __name__ == "__main__":
    main()
