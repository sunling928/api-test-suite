#!/usr/bin/env python3
"""
根据 API 变更生成受影响的测试用例
"""
import json
import os
from typing import Dict, Any, List


def load_change_report(file_path: str = "change_report.json") -> Dict[str, Any]:
    """加载变更报告"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_test_cases(changes: Dict[str, Any]) -> List[Dict[str, Any]]:
    """根据变更生成测试用例"""
    
    test_cases = []
    
    # 为新增端点生成测试用例
    for endpoint in changes.get("added_endpoints", []):
        test_case = {
            "name": f"test_{endpoint['method'].lower()}_{endpoint['path'].replace('/', '_').replace('{', '').replace('}', '')}",
            "endpoint": endpoint["path"],
            "method": endpoint["method"],
            "description": f"测试新增接口: {endpoint['summary']}",
            "priority": "high",
            "tags": ["new-api", "regression"]
        }
        test_cases.append(test_case)
    
    # 为修改端点生成回归测试
    for endpoint in changes.get("modified_endpoints", []):
        test_case = {
            "name": f"test_{endpoint['method'].lower()}_{endpoint['path'].replace('/', '_').replace('{', '').replace('}', '')}_modified",
            "endpoint": endpoint["path"],
            "method": endpoint["method"],
            "description": f"回归测试修改接口: {endpoint['summary']}",
            "priority": "high",
            "tags": ["modified-api", "regression"],
            "changes": endpoint.get("changes", {})
        }
        test_cases.append(test_case)
    
    # 为修改 Schema 生成测试用例
    for schema in changes.get("modified_schemas", []):
        test_case = {
            "name": f"test_schema_{schema['name']}_validation",
            "schema": schema["name"],
            "description": f"验证 Schema 变更: {schema['name']}",
            "priority": "medium",
            "tags": ["schema-change", "validation"],
            "changes": schema.get("changes", {})
        }
        test_cases.append(test_case)
    
    return test_cases


def generate_pytest_code(test_cases: List[Dict[str, Any]]) -> str:
    """生成 Pytest 代码"""
    
    code = '''"""
自动生成的回归测试用例
基于 API 变更检测
"""
import pytest
import requests
from conftest import assert_response, BASE_URL


class TestGeneratedRegression:
    """自动生成的回归测试"""
    
'''
    
    for i, tc in enumerate(test_cases, 1):
        code += f'''    @pytest.mark.{tc["tags"][0]}
    def {tc["name"]}(self, auth_headers):
        """
        {tc["description"]}
        优先级: {tc["priority"]}
        """
        # TODO: 根据实际接口实现测试逻辑
        pass

'''
    
    return code


def main():
    # 加载变更报告
    report = load_change_report()
    
    # 生成测试用例
    test_cases = generate_test_cases(report["changes"])
    
    # 生成 Pytest 代码
    pytest_code = generate_pytest_code(test_cases)
    
    # 保存生成的测试文件
    output_file = "test_generated_regression.py"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pytest_code)
    
    print(f"已生成 {len(test_cases)} 个测试用例: {output_file}")
    
    # 输出测试用例列表
    for tc in test_cases:
        print(f"  - {tc['name']} [{tc['priority']}]")


if __name__ == "__main__":
    main()
