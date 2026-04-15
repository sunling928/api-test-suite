"""
Pytest 配置文件 - 包含认证、参数化、断言等公共功能
"""
import pytest
import requests
import time
from typing import Dict, Any, Optional


# ==================== 配置 ====================
BASE_URL = "http://106.227.91.110:31000/api"
AUTH_CONFIG = {
    "username": "saber3",
    "password": "saber3_secret",  # Basic auth 凭证
    "auth_url": "/auth/login",  # 登录接口，请根据实际情况修改
}

# 用户提供的认证信息（2026-04-14 有效）
# 接口文档：https://s.apifox.cn/d13650af-5a6e-42e5-8c74-841714b5c1fa
PREDEFINED_AUTH = {
    "Authorization": "Basic c2FiZXI6c2FiZXJfc2VjcmV0",  # 从接口文档获取
    "Blade-Auth": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJibGFkZXguY24iLCJhdWQiOlsiYmxhZGV4Il0sInRva2VuX3R5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJzYWJlcjMiLCJ0ZW5hbnRfaWQiOiIwMDAwMDAiLCJ1c2VyX2lkIjoiMTEyMzU5ODgyMTczODY3NTIwMSIsImRlcHRfaWQiOiIyMDMxOTIyNDU0MTc1Mjc3MDU3IiwicG9zdF9pZCI6IjExMjM1OTg4MTc3Mzg2NzUyMDEiLCJyb2xlX2lkIjoiMTEyMzU5ODgxNjczODY3NTIwMSIsImFjY291bnQiOiJhZG1pbiIsInVzZXJfbmFtZSI6ImFkbWluIiwibmlja19uYW1lIjoi566h55CG5ZGYIiwicmVhbF9uYW1lIjoi566h55CG5ZGYiLCJyb2xlX25hbWUiOiJhZG1pbmlzdHJhdG9yIiwiZGV0YWlsIjp7InR5cGUiOiJ3ZWIifSwiZXhwIjoxNzc0ODQ0NTc1LCJuYmYiOjE3NzQ4NDA5MTfQ.WNl5pq38ah-OafHQq3IOALzv1zH-F1GDF9axOq-eZrg"  # 从接口文档获取
}


# ==================== 认证处理 ====================
class TokenManager:
    """Token 管理器 - 自动处理 Token 获取和刷新"""
    
    _instance = None
    _token: Optional[str] = None
    _token_expires_at: float = 0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_token(self, force_refresh: bool = False) -> str:
        """获取 Token，自动处理刷新"""
        if force_refresh or not self._token or time.time() >= self._token_expires_at:
            self._refresh_token()
        return self._token
    
    def _refresh_token(self):
        """刷新 Token - 请根据实际登录接口修改"""
        # 示例：实际使用时替换为真正的登录接口
        try:
            # 这里需要根据实际的登录接口来实现
            # 暂时使用预设的 token
            self._token = "YOUR_NEW_TOKEN_HERE"
            self._token_expires_at = time.time() + 3600  # 1小时后过期
        except Exception as e:
            pytest.fail(f"Token 刷新失败: {e}")
    
    def set_token(self, token: str, expires_in: int = 7200):
        """手动设置 Token"""
        self._token = token
        self._token_expires_at = time.time() + expires_in


# 全局 Token 管理器
token_manager = TokenManager()


# ==================== Fixtures ====================
@pytest.fixture(scope="session")
def base_url():
    """API 基础 URL"""
    return BASE_URL


@pytest.fixture(scope="session")
def auth_headers() -> Dict[str, str]:
    """认证头信息 - 使用预设认证信息"""
    return {
        "Authorization": PREDEFINED_AUTH["Authorization"],
        "Blade-Auth": PREDEFINED_AUTH["Blade-Auth"],
        "blade-requested-with": "BladeHttpRequest",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="function")
def client(base_url, auth_headers):
    """API 客户端"""
    return APIClient(base_url, auth_headers)


# ==================== API 客户端 ====================
class APIClient:
    """封装 API 请求，支持自动认证和错误处理"""
    
    def __init__(self, base_url: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(headers)
    
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """统一请求方法"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        return response
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST 请求"""
        return self.request("POST", endpoint, **kwargs)
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET 请求"""
        return self.request("GET", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT 请求"""
        return self.request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE 请求"""
        return self.request("DELETE", endpoint, **kwargs)
    
    def refresh_token(self, token: str, expires_in: int = 7200):
        """刷新 Token"""
        token_manager.set_token(token, expires_in)
        self.headers["Blade-Auth"] = f"Bearer {token}"
        self.session.headers.update(self.headers)


# ==================== 响应断言 ====================
class ResponseAssert:
    """响应断言封装"""
    
    def __init__(self, response: requests.Response):
        self.response = response
        self.data = response.json() if response.text else {}
    
    def status_code(self, code: int):
        """断言状态码"""
        assert self.response.status_code == code, \
            f"状态码断言失败: 期望 {code}, 实际 {self.response.status_code}"
        return self
    
    def success(self, msg: str = "操作成功"):
        """断言业务成功"""
        # 支持多种响应格式
        result_code = self.data.get("resultCode") or self.data.get("code") or self.data.get("success")
        
        # resultCode=0 或 code=0 或 success=True 表示成功
        is_success = result_code == 0 or result_code is True
        
        assert is_success, f"业务处理失败: {self.data.get('msg') or self.data.get('resultMsg') or msg}"
        return self
    
    def fail(self, msg: str = "操作失败"):
        """断言业务失败"""
        result_code = self.data.get("resultCode") or self.data.get("code")
        assert result_code != 0 and result_code is not True, \
            f"期望业务失败，但实际成功: {self.data}"
        return self
    
    def has_field(self, field: str):
        """断言响应包含指定字段"""
        assert field in self.data, f"响应缺少字段: {field}"
        return self
    
    def field_equals(self, field: str, value: Any):
        """断言字段值等于指定值"""
        assert self.data.get(field) == value, \
            f"字段 {field} 断言失败: 期望 {value}, 实际 {self.data.get(field)}"
        return self
    
    def field_not_empty(self, field: str):
        """断言字段值非空"""
        value = self.data.get(field)
        assert value is not None and value != "", \
            f"字段 {field} 不能为空"
        return self
    
    def contains(self, text: str):
        """断言响应包含指定文本"""
        assert text in str(self.data), f"响应不包含文本: {text}"
        return self
    
    def schema(self, schema: Dict[str, type]):
        """断言响应结构"""
        for field, expected_type in schema.items():
            assert field in self.data, f"响应缺少字段: {field}"
            assert isinstance(self.data[field], expected_type), \
                f"字段 {field} 类型错误: 期望 {expected_type}, 实际 {type(self.data[field])}"
        return self
    
    def print_response(self):
        """打印响应信息（用于调试）"""
        print(f"\n{'='*50}")
        print(f"状态码: {self.response.status_code}")
        print(f"响应头: {dict(self.response.headers)}")
        print(f"响应体: {self.data}")
        print(f"{'='*50}")
        return self


# 便捷函数
def assert_response(response: requests.Response) -> ResponseAssert:
    """创建响应断言对象"""
    return ResponseAssert(response)
