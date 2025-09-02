import requests
import json
from 登录 import post_request  # 导入登录模块

def delete_documents(start_number, end_number, form_id, cookies):
    """
    批量删除指定范围内的单据
    :param start_number: 起始单据编号
    :param end_number: 结束单据编号
    :param form_id: 表单ID
    :param cookies: 登录后的会话Cookie
    """
    url = "http://192.168.2.229/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Delete.common.kdsvc"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    for number in range(start_number, end_number + 1):
        bill_number = f"MRP{str(number).zfill(8)}"  # 格式化单据编号
        payload = {
            "parameters": [
                form_id,  # 表单标识
                json.dumps({"Numbers": [bill_number]})  # 单据编号
            ]
        }

        try:
            response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            if result.get("Result", {}).get("ResponseStatus", {}).get("IsSuccess"):
                print(f"单据 {bill_number} 删除成功")
            else:
                print(f"单据 {bill_number} 删除失败: {result}")
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")

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
    delete_documents(
        start_number=259227,
        end_number=352101,
        form_id="PLN_PLANORDER",  # 替换为实际的表单ID
        cookies=cookies
    )
