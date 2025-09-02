import requests
import json
import time  # Import time module for sleep functionality
from 登录 import post_request  # 导入登录模块
def delete_documents_in_batches(start_number, end_number, form_id, cookies, batch_size=50):
    """
    批量删除指定范围内的单据
    :param start_number: 起始单据编号
    :param end_number: 结束单据编号
    :param form_id: 表单ID
    :param cookies: 登录后的会话Cookie
    :param batch_size: 每次删除的单据数量
    """
    url = "http://192.168.2.229/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Delete.common.kdsvc"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    numbers = [f"MRP{str(number).zfill(8)}" for number in range(start_number, end_number + 1)]
    for i in range(0, len(numbers), batch_size):
        batch = numbers[i:i + batch_size]
        payload = {
            "parameters": [
                form_id,  # 表单标识
                json.dumps({"Numbers": batch})  # 批量单据编号
            ]
        }

        retries = 3  # 最大重试次数
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(payload))
                response.raise_for_status()
                result = response.json()
                if result.get("Result", {}).get("ResponseStatus", {}).get("IsSuccess"):
                    print(f"批量删除成功: {batch}")
                else:
                    print(f"批量删除失败: {result}")
                break  # 如果成功，跳出重试循环
            except requests.exceptions.RequestException as e:
                print(f"请求失败 (尝试 {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2)  # 等待 2 秒后重试
                else:
                    print(f"批量删除失败，已达到最大重试次数: {batch}")

if __name__ == "__main__":
    # 登录并获取会话信息
    login_result = post_request()
    if "error" in login_result:
        print("登录失败:", login_result["error"])
        exit()

    cookies = login_result.get("cookies", {})
    if not cookies:
        print("未获取到会话信息，请检查登录接口")
        exit()

    # 删除单据编号范围
    delete_documents_in_batches(
        start_number=288294,
        end_number=352101,
        form_id="PLN_PLANORDER",  # 替换为实际的表单ID
        cookies=cookies,
        batch_size=200
    )
