"""
订单提交接口测试套件 - 基于接口文档自动生成
接口：POST /mini-operate/api/order/submitOrder
文档：https://s.apifox.cn/d13650af-5a6e-42e5-8c74-841714b5c1fa
"""
import pytest
import requests
import time
from typing import Dict, Any
from conftest import assert_response, BASE_URL


# ==================== 配置 ====================
ENDPOINT = "/mini-operate/api/order/submitOrder"
URL = f"{BASE_URL}{ENDPOINT}"


# ==================== 测试数据 ====================
class OrderTestData:
    """订单测试数据生成器"""
    
    @staticmethod
    def valid_order() -> Dict[str, Any]:
        """有效的订单数据"""
        return {
            "abilityProId": "test_ability_001",
            "orderNumber": f"ORD{int(time.time())}",
            "signType": 1,  # 签约类型：1-签约
            "freeTrialFlag": 0,  # 订单类型：0-正式
            "freeDays": 0,
            "productCode": "PROD001",
            "productCount": 1,
            "productTime": 12,
            "productType": 1,  # 订单类别：1-原子订单
            "projectCode": "PRJ001",
            "projectName": "测试项目",
            "provinceName": "北京",
            "userName": "test_user",
            "userMail": "test@example.com",
            "custId": "CUST001",
            "requestId": f"REQ{int(time.time())}",
            "capId": "CAP001",
            "callbackUrl": "http://example.com/callback",
            "isAdminAccount": "0",
            "usageInfoNum": 1,
            "costInstNo": "INST001",
            "costInstName": "测试套餐",
            "costSpecs": "标准版"
        }
    
    @staticmethod
    def trial_order() -> Dict[str, Any]:
        """试用订单数据"""
        return {
            "abilityProId": "test_ability_002",
            "orderNumber": f"TRIAL{int(time.time())}",
            "signType": 1,
            "freeTrialFlag": 1,  # 试用
            "freeDays": 30,
            "productCode": "PROD002",
            "productCount": 1,
            "productTime": 1,
            "productType": 2,  # 试用订单
            "projectCode": "PRJ002",
            "projectName": "试用项目",
            "provinceName": "上海",
            "userName": "trial_user",
            "userMail": "trial@example.com",
            "custId": "CUST002",
            "requestId": f"REQ{int(time.time())}",
            "callbackUrl": "http://example.com/callback"
        }
    
    @staticmethod
    def termination_order() -> Dict[str, Any]:
        """解约订单数据"""
        return {
            "abilityProId": "test_ability_003",
            "orderNumber": f"TERM{int(time.time())}",
            "signType": 2,  # 解约
            "freeTrialFlag": 3,  # 解约
            "productCode": "PROD003",
            "productCount": 1,
            "productTime": 0,
            "projectCode": "PRJ003",
            "custId": "CUST003",
            "requestId": f"REQ{int(time.time())}"
        }
    
    @staticmethod
    def missing_required_fields() -> Dict[str, Any]:
        """缺少必填字段"""
        return {
            "productCode": "PROD001"
            # 缺少其他必填字段
        }
    
    @staticmethod
    def invalid_sign_type() -> Dict[str, Any]:
        """无效的签约类型"""
        data = OrderTestData.valid_order()
        data["signType"] = 999  # 无效值
        return data
    
    @staticmethod
    def negative_product_count() -> Dict[str, Any]:
        """负数的订购数量"""
        data = OrderTestData.valid_order()
        data["productCount"] = -1
        return data


# ==================== 订单提交测试 ====================
class TestOrderSubmit:
    """订单提交接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, auth_headers):
        """设置测试环境"""
        self.headers = auth_headers
    
    # ==================== 正向测试 ====================
    def test_submit_order_success(self):
        """测试提交正式订单 - 成功"""
        payload = OrderTestData.valid_order()
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        assert_response(response) \
            .status_code(200) \
            .has_field("resultCode") \
            .print_response()
        
        # 验证响应结构
        data = response.json()
        assert "resultCode" in data or "code" in data, "响应缺少结果码"
    
    def test_submit_trial_order(self):
        """测试提交试用订单"""
        payload = OrderTestData.trial_order()
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        assert_response(response) \
            .status_code(200) \
            .print_response()
    
    def test_submit_termination_order(self):
        """测试提交解约订单"""
        payload = OrderTestData.termination_order()
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        assert_response(response) \
            .status_code(200) \
            .print_response()
    
    # ==================== 参数化测试 ====================
    @pytest.mark.parametrize("sign_type,flag,description", [
        (1, 0, "签约-正式订单"),
        (1, 1, "签约-试用订单"),
        (2, 3, "解约订单"),
        (3, 2, "未签约-未签试用"),
    ])
    def test_submit_order_with_different_types(self, sign_type, flag, description):
        """测试不同类型的订单"""
        payload = OrderTestData.valid_order()
        payload["signType"] = sign_type
        payload["freeTrialFlag"] = flag
        payload["orderNumber"] = f"ORD_{sign_type}_{flag}_{int(time.time())}"
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        print(f"\n测试场景: {description}")
        assert_response(response) \
            .status_code(200) \
            .print_response()
    
    @pytest.mark.parametrize("product_count,product_time", [
        (1, 1),    # 最小值
        (1, 12),   # 常见值
        (10, 24),  # 较大值
        (100, 36), # 大批量
    ])
    def test_submit_order_with_different_quantities(self, product_count, product_time):
        """测试不同数量和时长的订单"""
        payload = OrderTestData.valid_order()
        payload["productCount"] = product_count
        payload["productTime"] = product_time
        payload["orderNumber"] = f"ORD_{product_count}_{product_time}_{int(time.time())}"
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        print(f"\n数量: {product_count}, 时长: {product_time}")
        assert_response(response) \
            .status_code(200) \
            .print_response()
    
    # ==================== 异常测试 ====================
    def test_submit_order_missing_required_fields(self):
        """测试缺少必填字段"""
        payload = OrderTestData.missing_required_fields()
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        print(f"\n缺少必填字段响应: {response.status_code}")
        # 可能返回 400 或 200 带错误码
        assert response.status_code in [200, 400, 422]
    
    def test_submit_order_invalid_sign_type(self):
        """测试无效的签约类型"""
        payload = OrderTestData.invalid_sign_type()
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        print(f"\n无效签约类型响应: {response.json()}")
        assert response.status_code in [200, 400]
    
    def test_submit_order_negative_count(self):
        """测试负数的订购数量"""
        payload = OrderTestData.negative_product_count()
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        print(f"\n负数数量响应: {response.json()}")
        assert response.status_code in [200, 400, 422]
    
    # ==================== 空值测试 ====================
    @pytest.mark.parametrize("field,value", [
        ("productCode", ""),
        ("productCode", None),
        ("custId", ""),
        ("custId", None),
        ("projectCode", ""),
    ])
    def test_submit_order_empty_fields(self, field, value):
        """测试空值字段"""
        payload = OrderTestData.valid_order()
        payload[field] = value
        payload["orderNumber"] = f"ORD_EMPTY_{field}_{int(time.time())}"
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        print(f"\n字段 {field} = {value} 的响应: {response.json()}")
        assert response.status_code in [200, 400, 422]
    
    # ==================== 边界值测试 ====================
    @pytest.mark.parametrize("product_count", [0, 1, 999999])
    def test_submit_order_boundary_count(self, product_count):
        """测试订购数量边界值"""
        payload = OrderTestData.valid_order()
        payload["productCount"] = product_count
        payload["orderNumber"] = f"ORD_BOUND_{product_count}_{int(time.time())}"
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        print(f"\n边界值 {product_count} 响应: {response.json()}")
        assert response.status_code == 200


# ==================== 认证测试 ====================
class TestAuthentication:
    """认证相关测试"""
    
    def test_without_authorization(self):
        """测试缺少 Authorization 头"""
        headers = {
            "Content-Type": "application/json",
            "Blade-Auth": "bearer test_token",
            "blade-requested-with": "BladeHttpRequest"
        }
        
        payload = OrderTestData.valid_order()
        response = requests.post(URL, json=payload, headers=headers)
        
        print(f"\n无 Authorization 响应: {response.status_code}")
        assert response.status_code in [401, 403]
    
    def test_without_blade_auth(self):
        """测试缺少 Blade-Auth 头"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic c2FiZXI6c2FiZXJfc2VjcmV0",
            "blade-requested-with": "BladeHttpRequest"
        }
        
        payload = OrderTestData.valid_order()
        response = requests.post(URL, json=payload, headers=headers)
        
        print(f"\n无 Blade-Auth 响应: {response.status_code}")
        assert response.status_code in [401, 403]
    
    def test_invalid_token(self):
        """测试无效 Token"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic invalid",
            "Blade-Auth": "bearer invalid_token",
            "blade-requested-with": "BladeHttpRequest"
        }
        
        payload = OrderTestData.valid_order()
        response = requests.post(URL, json=payload, headers=headers)
        
        print(f"\n无效 Token 响应: {response.status_code}")
        assert response.status_code in [401, 403]
    
    def test_expired_token(self):
        """测试过期 Token（模拟）"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic c2FiZXI6c2FiZXJfc2VjcmV0",
            "Blade-Auth": "bearer expired_token_placeholder",
            "blade-requested-with": "BladeHttpRequest"
        }
        
        payload = OrderTestData.valid_order()
        response = requests.post(URL, json=payload, headers=headers)
        
        print(f"\n过期 Token 响应: {response.status_code}")
        # 根据实际 API 行为调整断言


# ==================== 响应格式测试 ====================
class TestResponseFormat:
    """响应格式验证"""
    
    @pytest.fixture(autouse=True)
    def setup(self, auth_headers):
        self.headers = auth_headers
    
    def test_response_has_result_code(self):
        """测试响应包含结果码"""
        payload = OrderTestData.valid_order()
        response = requests.post(URL, json=payload, headers=self.headers)
        
        data = response.json()
        assert "resultCode" in data or "code" in data, \
            "响应应包含 resultCode 或 code 字段"
    
    def test_response_has_message(self):
        """测试响应包含消息"""
        payload = OrderTestData.valid_order()
        response = requests.post(URL, json=payload, headers=self.headers)
        
        data = response.json()
        assert "resultMsg" in data or "msg" in data, \
            "响应应包含 resultMsg 或 msg 字段"
    
    def test_response_content_type(self):
        """测试响应 Content-Type"""
        payload = OrderTestData.valid_order()
        response = requests.post(URL, json=payload, headers=self.headers)
        
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, \
            f"期望 Content-Type 为 application/json, 实际为 {content_type}"


# ==================== 性能测试 ====================
class TestPerformance:
    """性能测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, auth_headers):
        self.headers = auth_headers
    
    def test_response_time(self):
        """测试响应时间"""
        payload = OrderTestData.valid_order()
        
        start_time = time.time()
        response = requests.post(URL, json=payload, headers=self.headers)
        elapsed_ms = (time.time() - start_time) * 1000
        
        print(f"\n响应时间: {elapsed_ms:.2f}ms")
        
        assert response.status_code == 200
        assert elapsed_ms < 5000, f"响应时间过长: {elapsed_ms:.2f}ms"
    
    @pytest.mark.parametrize("concurrent", [1, 3, 5])
    def test_concurrent_requests(self, concurrent):
        """测试并发请求"""
        import concurrent.futures
        
        def make_request(index):
            payload = OrderTestData.valid_order()
            payload["orderNumber"] = f"ORD_CONCURRENT_{index}_{int(time.time())}"
            return requests.post(URL, json=payload, headers=self.headers)
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
            futures = [executor.submit(make_request, i) for i in range(concurrent)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        print(f"\n{concurrent} 个并发请求完成时间: {elapsed_ms:.2f}ms")
        
        # 验证所有请求都成功
        for i, response in enumerate(results):
            assert response.status_code == 200, f"请求 {i} 失败: {response.status_code}"


# ==================== 数据驱动测试 ====================
class TestDataDriven:
    """数据驱动测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, auth_headers):
        self.headers = auth_headers
    
    @pytest.mark.parametrize("test_case", [
        {
            "name": "正式签约订单",
            "data": {
                "signType": 1, "freeTrialFlag": 0,
                "productCount": 1, "productTime": 12
            }
        },
        {
            "name": "试用订单",
            "data": {
                "signType": 1, "freeTrialFlag": 1,
                "freeDays": 30, "productCount": 1, "productTime": 1
            }
        },
        {
            "name": "解约订单",
            "data": {
                "signType": 2, "freeTrialFlag": 3,
                "productCount": 1, "productTime": 0
            }
        },
    ], ids=lambda tc: tc["name"])
    def test_order_scenarios(self, test_case):
        """测试不同业务场景"""
        payload = OrderTestData.valid_order()
        payload.update(test_case["data"])
        payload["orderNumber"] = f"ORD_{test_case['name']}_{int(time.time())}"
        
        response = requests.post(URL, json=payload, headers=self.headers)
        
        print(f"\n场景: {test_case['name']}")
        assert_response(response) \
            .status_code(200) \
            .print_response()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short", "--alluredir=./allure-results"])
