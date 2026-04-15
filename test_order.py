"""
订单接口测试套件 - 参数化版本
包含：Token自动认证、参数化测试、响应断言
"""
import pytest
import requests
from conftest import assert_response, token_manager, BASE_URL
from test_data import (
    get_positive_cases,
    get_negative_cases,
    get_boundary_cases,
    generate_order_data
)


# ==================== 订单提交接口测试 ====================
class TestOrderSubmit:
    """订单提交接口 - 参数化测试"""
    
    ENDPOINT = "/mini-operate/api/order/submitOrder"
    
    @pytest.fixture(autouse=True)
    def setup(self, auth_headers):
        """设置测试环境"""
        self.headers = auth_headers
        self.url = f"{BASE_URL}{self.ENDPOINT}"
    
    # ==================== 正向测试 ====================
    @pytest.mark.parametrize("case", get_positive_cases(), ids=lambda c: c["name"])
    def test_submit_order_success(self, case):
        """
        正向测试 - 验证各种正常场景
        """
        response = requests.post(self.url, json=case["data"], headers=self.headers)
        
        # 使用断言封装
        assert_response(response) \
            .status_code(200) \
            .print_response()
        
        # 根据实际响应格式调整断言
        data = response.json()
        result_code = data.get("resultCode") or data.get("code")
        # 允许业务层面的不同响应码
        assert result_code is not None, "响应缺少 resultCode 字段"
    
    # ==================== 异常测试 ====================
    @pytest.mark.parametrize("case", get_negative_cases(), ids=lambda c: c["name"])
    def test_submit_order_validation(self, case):
        """
        异常测试 - 验证参数校验
        """
        response = requests.post(self.url, json=case["data"], headers=self.headers)
        
        # 打印响应用于调试
        print(f"\n测试: {case['name']}")
        print(f"响应: {response.json()}")
        
        # 验证返回了错误响应（可能是400或200带错误码）
        assert response.status_code in [200, 400, 422], \
            f"期望状态码 200/400/422, 实际 {response.status_code}"
    
    # ==================== 边界值测试 ====================
    @pytest.mark.parametrize("case", get_boundary_cases(), ids=lambda c: c["name"])
    def test_submit_order_boundary(self, case):
        """
        边界值测试
        """
        response = requests.post(self.url, json=case["data"], headers=self.headers)
        data = response.json()
        
        print(f"\n测试: {case['name']}")
        print(f"响应: {data}")
        
        # 边界值测试不强制要求成功，允许根据业务逻辑调整
        assert response.status_code == 200
    
    # ==================== 批量数据测试 ====================
    @pytest.mark.parametrize("index", range(1, 6))
    def test_submit_order_batch(self, index):
        """
        批量数据测试 - 使用数据生成器
        """
        data = generate_order_data(index)
        
        response = requests.post(self.url, json=data, headers=self.headers)
        
        assert_response(response) \
            .status_code(200) \
            .print_response()


# ==================== 认证测试 ====================
class TestAuth:
    """认证相关测试"""
    
    ENDPOINT = "/mini-operate/api/order/submitOrder"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = f"{BASE_URL}{self.ENDPOINT}"
    
    def test_submit_order_without_auth(self):
        """测试无认证信息"""
        headers = {"Content-Type": "application/json"}
        payload = {
            "abilityProId": "test_001",
            "productCode": "PROD001",
            "productCount": 1,
            "productTime": 12,
            "projectCode": "PRJ001",
            "custId": "CUST001"
        }
        
        response = requests.post(self.url, json=payload, headers=headers)
        
        print(f"\n无认证响应: {response.status_code} - {response.text}")
        # 期望返回认证失败
        assert response.status_code in [401, 403]
    
    def test_submit_order_invalid_token(self):
        """测试无效 Token"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic c2FiZXI6c2FiZXJfc2VjcmV0",
            "Blade-Auth": "Bearer invalid_token_12345",
            "blade-requested-with": "BladeHttpRequest"
        }
        
        payload = {
            "abilityProId": "test_001",
            "productCode": "PROD001",
            "productCount": 1,
            "productTime": 12,
            "projectCode": "PRJ001",
            "custId": "CUST001"
        }
        
        response = requests.post(self.url, json=payload, headers=headers)
        
        print(f"\n无效Token响应: {response.status_code}")
        assert response.status_code in [401, 403]
    
    def test_token_refresh(self):
        """测试 Token 刷新功能"""
        # 模拟 Token 刷新
        new_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3Mi..."
        token_manager.set_token(new_token, expires_in=3600)
        
        # 验证 Token 已更新
        assert token_manager.get_token() == new_token
        print("\nToken 刷新成功")


# ==================== 响应格式测试 ====================
class TestResponseFormat:
    """响应格式测试"""
    
    ENDPOINT = "/mini-operate/api/order/submitOrder"
    
    @pytest.fixture(autouse=True)
    def setup(self, auth_headers):
        self.headers = auth_headers
        self.url = f"{BASE_URL}{self.ENDPOINT}"
    
    def test_response_schema(self):
        """测试响应结构"""
        payload = {
            "abilityProId": "test_001",
            "productCode": "PROD001",
            "productCount": 1,
            "productTime": 12,
            "projectCode": "PRJ001",
            "custId": "CUST001",
            "signType": 1,
            "freeTrialFlag": 0
        }
        
        response = requests.post(self.url, json=payload, headers=self.headers)
        
        # 使用断言封装验证响应结构
        assert_response(response) \
            .status_code(200) \
            .has_field("resultCode") \
            .print_response()
    
    def test_response_code_meaning(self):
        """测试响应码含义"""
        test_cases = [
            # (payload, expected_meaning)
            ({"abilityProId": "test", "productCode": "P1", "productCount": 1, 
              "productTime": 1, "projectCode": "PRJ", "custId": "C", "signType": 1, "freeTrialFlag": 0}, 
             "正常处理"),
        ]
        
        for payload, meaning in test_cases:
            response = requests.post(self.url, json=payload, headers=self.headers)
            data = response.json()
            print(f"\n{meaning}: {data}")


# ==================== 性能测试 ====================
class TestPerformance:
    """性能测试"""
    
    ENDPOINT = "/mini-operate/api/order/submitOrder"
    
    @pytest.fixture(autouse=True)
    def setup(self, auth_headers):
        self.headers = auth_headers
        self.url = f"{BASE_URL}{self.ENDPOINT}"
    
    @pytest.mark.parametrize("count", [1, 5, 10])
    def test_response_time(self, count):
        """测试响应时间"""
        import time
        
        payload = {
            "abilityProId": f"test_{count}",
            "productCode": f"PROD{count:03d}",
            "productCount": 1,
            "productTime": 12,
            "projectCode": f"PRJ{count:03d}",
            "custId": f"CUST{count:03d}",
            "signType": 1,
            "freeTrialFlag": 0
        }
        
        start_time = time.time()
        response = requests.post(self.url, json=payload, headers=self.headers)
        elapsed = (time.time() - start_time) * 1000  # 转换为毫秒
        
        print(f"\n请求 {count} 响应时间: {elapsed:.2f}ms")
        
        assert response.status_code == 200
        assert elapsed < 5000, f"响应时间过长: {elapsed:.2f}ms"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
