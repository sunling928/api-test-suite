"""
测试数据 - 参数化配置
"""
import pytest
from typing import Dict, Any, List


# ==================== 订单数据模板 ====================
ORDER_DATA_TEMPLATE = {
    "abilityProId": "test_ability_{index}",
    "productCode": "PROD{index:03d}",
    "productCount": 1,
    "productTime": 12,
    "productType": 1,
    "projectCode": "PRJ{index:03d}",
    "projectName": "测试项目{index}",
    "provinceName": "北京市",
    "userName": "test_user_{index}",
    "userMail": "test{index}@example.com",
    "custId": "CUST{index:03d}",
    "signType": 1,
    "freeTrialFlag": 0
}


# ==================== 正向测试数据 ====================
POSITIVE_TEST_CASES = [
    {
        "name": "最小必填参数-签约订单",
        "data": {
            "abilityProId": "ability_001",
            "productCode": "PROD001",
            "productCount": 1,
            "productTime": 12,
            "productType": 1,
            "projectCode": "PRJ001",
            "projectName": "签约测试项目",
            "provinceName": "北京市",
            "userName": "user001",
            "userMail": "user001@example.com",
            "custId": "CUST001",
            "signType": 1,
            "freeTrialFlag": 0
        },
        "expected": {"success": True}
    },
    {
        "name": "完整参数-试用订单",
        "data": {
            "abilityProId": "ability_002",
            "orderNumber": None,
            "signType": 1,
            "freeTrialFlag": 1,
            "freeDays": 7,
            "productCode": "PROD002",
            "productCount": 10,
            "productTime": 24,
            "productType": 2,
            "projectCode": "PRJ002",
            "projectName": "完整试用项目",
            "provinceName": "上海市",
            "userName": "user002",
            "userMail": "user002@example.com",
            "custId": "CUST002",
            "requestId": "REQ123456",
            "capId": "CAP001",
            "callbackUrl": "https://example.com/callback",
            "isAdminAccount": "0",
            "usageInfoNum": 100,
            "costInstNo": "COST001",
            "costInstName": "基础套餐",
            "costSpecs": "标准规格"
        },
        "expected": {"success": True}
    },
    {
        "name": "解约订单",
        "data": {
            "abilityProId": "ability_003",
            "productCode": "PROD003",
            "productCount": 1,
            "productTime": 0,
            "productType": 1,
            "projectCode": "PRJ003",
            "projectName": "解约测试项目",
            "provinceName": "广东省",
            "userName": "user003",
            "userMail": "user003@example.com",
            "custId": "CUST003",
            "signType": 2,
            "freeTrialFlag": 3
        },
        "expected": {"success": True}
    },
    {
        "name": "管理员账号开通",
        "data": {
            "abilityProId": "ability_004",
            "productCode": "PROD004",
            "productCount": 5,
            "productTime": 36,
            "productType": 1,
            "projectCode": "PRJ004",
            "projectName": "管理员开通项目",
            "provinceName": "浙江省",
            "userName": "admin",
            "userMail": "admin@example.com",
            "custId": "CUST004",
            "signType": 1,
            "freeTrialFlag": 0,
            "isAdminAccount": "1",
            "adminAccount": "admin_user"
        },
        "expected": {"success": True}
    },
]


# ==================== 异常测试数据 ====================
NEGATIVE_TEST_CASES = [
    {
        "name": "缺少abilityProId",
        "data": {
            "productCode": "PROD001",
            "productCount": 1,
            "projectCode": "PRJ001",
            "custId": "CUST001"
        },
        "expected": {"success": False, "error_type": "missing_field"}
    },
    {
        "name": "缺少productCode",
        "data": {
            "abilityProId": "ability_001",
            "productCount": 1,
            "projectCode": "PRJ001",
            "custId": "CUST001"
        },
        "expected": {"success": False, "error_type": "missing_field"}
    },
    {
        "name": "productCount为负数",
        "data": {
            "abilityProId": "ability_001",
            "productCode": "PROD001",
            "productCount": -1,
            "productTime": 12,
            "projectCode": "PRJ001",
            "custId": "CUST001"
        },
        "expected": {"success": False, "error_type": "invalid_value"}
    },
    {
        "name": "productTime为负数",
        "data": {
            "abilityProId": "ability_001",
            "productCode": "PROD001",
            "productCount": 1,
            "productTime": -12,
            "projectCode": "PRJ001",
            "custId": "CUST001"
        },
        "expected": {"success": False, "error_type": "invalid_value"}
    },
    {
        "name": "signType无效值",
        "data": {
            "abilityProId": "ability_001",
            "productCode": "PROD001",
            "productCount": 1,
            "productTime": 12,
            "projectCode": "PRJ001",
            "custId": "CUST001",
            "signType": 999
        },
        "expected": {"success": False, "error_type": "invalid_value"}
    },
    {
        "name": "邮箱格式错误",
        "data": {
            "abilityProId": "ability_001",
            "productCode": "PROD001",
            "productCount": 1,
            "productTime": 12,
            "projectCode": "PRJ001",
            "custId": "CUST001",
            "userMail": "invalid_email"
        },
        "expected": {"success": False, "error_type": "invalid_format"}
    },
]


# ==================== 边界值测试数据 ====================
BOUNDARY_TEST_CASES = [
    {
        "name": "productCount最小值_1",
        "data": {**ORDER_DATA_TEMPLATE, "productCount": 1},
        "expected": {"success": True}
    },
    {
        "name": "productCount较大值_10000",
        "data": {**ORDER_DATA_TEMPLATE, "productCount": 10000},
        "expected": {"success": True}
    },
    {
        "name": "productTime最小值_1",
        "data": {**ORDER_DATA_TEMPLATE, "productTime": 1},
        "expected": {"success": True}
    },
    {
        "name": "freeDays最大值_365",
        "data": {**ORDER_DATA_TEMPLATE, "freeDays": 365, "freeTrialFlag": 1},
        "expected": {"success": True}
    },
    {
        "name": "空字符串字段",
        "data": {**ORDER_DATA_TEMPLATE, "projectName": ""},
        "expected": {"success": False}
    },
]


# ==================== 数据生成器 ====================
def generate_order_data(index: int, **overrides) -> Dict[str, Any]:
    """生成订单数据"""
    data = {
        k: v.format(index=index) if isinstance(v, str) and "{index}" in v else v
        for k, v in ORDER_DATA_TEMPLATE.items()
    }
    data.update(overrides)
    return data


def get_positive_cases() -> List[Dict]:
    """获取正向测试用例"""
    return POSITIVE_TEST_CASES


def get_negative_cases() -> List[Dict]:
    """获取异常测试用例"""
    return NEGATIVE_TEST_CASES


def get_boundary_cases() -> List[Dict]:
    """获取边界值测试用例"""
    return BOUNDARY_TEST_CASES
