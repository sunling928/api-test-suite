#!/usr/bin/env python3
"""
API 变更检测脚本
检测 OpenAPI 规范的变化，生成变更报告
"""
import yaml
import json
import argparse
from deepdiff import DeepDiff
from typing import Dict, Any, List


def load_yaml(file_path: str) -> Dict[str, Any]:
    """加载 YAML 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def detect_api_changes(old_spec: Dict[str, Any], new_spec: Dict[str, Any]) -> Dict[str, Any]:
    """检测 API 变更"""
    
    changes = {
        "added_endpoints": [],
        "removed_endpoints": [],
        "modified_endpoints": [],
        "added_parameters": [],
        "removed_parameters": [],
        "modified_parameters": [],
        "added_schemas": [],
        "removed_schemas": [],
        "modified_schemas": []
    }
    
    # 检测路径变化
    old_paths = old_spec.get('paths', {})
    new_paths = new_spec.get('paths', {})
    
    # 新增的端点
    for path, methods in new_paths.items():
        if path not in old_paths:
            for method, details in methods.items():
                changes["added_endpoints"].append({
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get('summary', '')
                })
    
    # 删除的端点
    for path, methods in old_paths.items():
        if path not in new_paths:
            for method, details in methods.items():
                changes["removed_endpoints"].append({
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get('summary', '')
                })
    
    # 修改的端点
    for path, methods in new_paths.items():
        if path in old_paths:
            old_methods = old_paths[path]
            for method, new_details in methods.items():
                if method in old_methods:
                    old_details = old_methods[method]
                    
                    # 使用 DeepDiff 检测详细变化
                    diff = DeepDiff(old_details, new_details, ignore_order=True)
                    
                    if diff:
                        changes["modified_endpoints"].append({
                            "path": path,
                            "method": method.upper(),
                            "summary": new_details.get('summary', ''),
                            "changes": diff.to_dict()
                        })
    
    # 检测 Schema 变化
    old_schemas = old_spec.get('components', {}).get('schemas', {})
    new_schemas = new_spec.get('components', {}).get('schemas', {})
    
    # 新增的 Schema
    for name, schema in new_schemas.items():
        if name not in old_schemas:
            changes["added_schemas"].append({
                "name": name,
                "type": schema.get('type', 'object')
            })
    
    # 删除的 Schema
    for name, schema in old_schemas.items():
        if name not in new_schemas:
            changes["removed_schemas"].append({
                "name": name,
                "type": schema.get('type', 'object')
            })
    
    # 修改的 Schema
    for name, new_schema in new_schemas.items():
        if name in old_schemas:
            old_schema = old_schemas[name]
            diff = DeepDiff(old_schema, new_schema, ignore_order=True)
            
            if diff:
                changes["modified_schemas"].append({
                    "name": name,
                    "changes": diff.to_dict()
                })
    
    return changes


def generate_test_plan(changes: Dict[str, Any]) -> Dict[str, Any]:
    """根据变更生成测试计划"""
    
    test_plan = {
        "affected_tests": [],
        "new_tests_needed": [],
        "priority": "medium"
    }
    
    # 根据变更类型确定测试重点
    if changes["added_endpoints"]:
        test_plan["new_tests_needed"].extend([
            f"test_{endpoint['method'].lower()}_{endpoint['path'].replace('/', '_')}"
            for endpoint in changes["added_endpoints"]
        ])
        test_plan["priority"] = "high"
    
    if changes["modified_endpoints"]:
        test_plan["affected_tests"].extend([
            f"test_submit_order_success"  # 示例：具体测试用例
            # 根据实际变更的端点添加更多测试
        ])
        test_plan["priority"] = "high"
    
    if changes["modified_schemas"]:
        test_plan["affected_tests"].append("test_response_schema")
        test_plan["priority"] = "medium"
    
    return test_plan


def main():
    parser = argparse.ArgumentParser(description="检测 API 变更并生成报告")
    parser.add_argument("--old-spec", required=True, help="旧的 OpenAPI 规范文件")
    parser.add_argument("--new-spec", required=True, help="新的 OpenAPI 规范文件")
    parser.add_argument("--output", default="change_report.json", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 加载规范文件
    old_spec = load_yaml(args.old_spec)
    new_spec = load_yaml(args.new_spec)
    
    # 检测变更
    changes = detect_api_changes(old_spec, new_spec)
    
    # 生成测试计划
    test_plan = generate_test_plan(changes)
    
    # 合并报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "old_spec": args.old_spec,
        "new_spec": args.new_spec,
        "changes": changes,
        "test_plan": test_plan,
        "summary": {
            "total_changes": sum(len(v) for v in changes.values()),
            "breaking_changes": len(changes["removed_endpoints"]) + len(changes["modified_endpoints"]),
            "new_features": len(changes["added_endpoints"])
        }
    }
    
    # 保存报告
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"API 变更报告已生成: {args.output}")
    
    # 输出摘要
    summary = report["summary"]
    print(f"\n变更摘要:")
    print(f"  - 总变更数: {summary['total_changes']}")
    print(f"  - 破坏性变更: {summary['breaking_changes']}")
    print(f"  - 新增功能: {summary['new_features']}")
    
    # 如果有破坏性变更，以非零状态码退出
    if summary["breaking_changes"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    import sys
    from datetime import datetime
    main()
