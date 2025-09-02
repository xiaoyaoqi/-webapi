import requests
import hashlib
import time

def generate_signature(acct_id, username, app_id, app_secret):
    """
    生成签名信息
    """
    timestamp = int(time.time())  # 获取当前时间戳
    sign_array = [acct_id, username, app_id, app_secret, str(timestamp)]
    sign_array.sort()  # 按字典序排序
    sign_string = ''.join(sign_array)  # 拼接成字符串
    sha256 = hashlib.sha256()  # 使用 SHA256 算法
    sha256.update(sign_string.encode('utf-8'))
    signature = sha256.hexdigest()
    return signature, timestamp

def post_request():
    url = "http://localhost/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.AuthService.LoginBySign.common.kdsvc"
    
    # 替换为实际的账套ID、用户名、应用ID和应用密钥
    acct_id = "67f63bfb8a7c61"
    username = "Administrator"
    app_id = "308922_WddCT+hPTIgfwVUFXdWqR7SJ3L0U6rmF"
    app_secret = "03266992ee2642adb8ea9f14f881bfd3"

    # 生成签名和时间戳
    signature, timestamp = generate_signature(acct_id, username, app_id, app_secret)

    # 构造请求数据
    payload = {
        "acctID": acct_id,
        "username": username,
        "appId": app_id,
        "timestamp": timestamp,
        "sign": signature,
        "lcid": 2052  # 语言标识符，2052 表示简体中文
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # 检查 HTTP 请求是否成功
        # 提取 Cookie
        cookies = response.cookies.get_dict()
        return {"data": response.json(), "cookies": cookies}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = post_request()
    print(result)
